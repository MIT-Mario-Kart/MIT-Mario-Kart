#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#include <uri/UriBraces.h>
#include <uri/UriRegex.h>
#include <Servo.h>

#include <math.h>
#include <stdlib.h>

#ifndef STASSID
#define STASSID "Rok's iPhone"
#define STAPSK "babalilo"
#endif

// #define SERVER_IP "172.20.10.2"
#define SERVER_PORT 8888

#define ID "CAR1"

#define START_ORIENTATION M_PI/2            // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100                 // ~ 1.8 deg
#define MAX_ORIENTATION M_PI
#define MIN_ORIENTATION -MAX_ORIENTATION    // -180 deg <= orientation <= 180 deg
#define ANGLE_PRECISION 1                   // In degrees (if angle is within ± ANGLE_PRECISION 
                                            // it doesn't get updated)
#define MAX_VELOCITY 0.025
#define SLOWDOWN_DECEL 0.0125
#define STOP_DECEL 0.025
#define ACC_UNIT 0.025
#define MAX_ACC 0.025

// 1 Unit (along x or y) =~ 10 cm irl
#define START_X 0   
#define START_Y 0

#define STOP -2
#define SLOWDOWN -1
#define MAINTAIN_VELOCITY 0
#define ACCELERATE 1

#define PIN_D2_FORWARD 4
#define PIN_D1_REVERSE 5
#define SERVO_PIN 15

const char *ssid = STASSID;
const char *password = STAPSK;

Servo myservo;
int port = 9999;  //Port number
WiFiServer server(port);

IPAddress SERVER_IP(172,20,10,2);
int init_val = 1;
int interaction_index = 0;
// Using doubles for extra precision (lol)
double coord_x = START_X;
double coord_y = START_Y;
double dir = START_ORIENTATION;
double velocity_x = 0;
double velocity_y = 0;
double acc_x = 0;
double acc_y = 0;


boolean connected = false;

void WiFiEvent(WiFiEvent_t event) {
    switch(event) {
    case 3: // WL_CONNECTED 
        Serial.println("WiFi connected");
        Serial.println("IP address: ");
        Serial.println(WiFi.localIP());
        connected = true;
        break;
    case 6: // WL_DISCONNECTED 
        Serial.println("WiFi lost connection");
        connected = false;
        break;
    }
}

void setup(void) {
  pinMode(PIN_D2_FORWARD,OUTPUT); // D2 F
  pinMode(PIN_D1_REVERSE,OUTPUT); // D1 R
  myservo.attach(SERVO_PIN); // D8
  // 172.20.10.5

  Serial.begin(115200);
  WiFi.disconnect(true);
  delay(1000);
  WiFi.onEvent(WiFiEvent); // update connected variable method based on event
  WiFi.mode(WIFI_STA); 
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
  Serial.println("Started server");
  if (MDNS.begin("esp8266")) { Serial.println("MDNS responder started"); }
  send_coords();
}

void loop(void) {
    WiFiClient client = server.available();
    
    if(!connected){  
        update_movements(0, -2); // STOP the car 
    } else {
    // if (client) {
        
        char packet[255];
        int i = 0;
        
        // while(client.connected()){
            while(client.available()>0){
                // read data from the connected client
                packet[i] = client.read(); 
                ++i;
            }
            int desired_angle = atoi(packet);
            if (desired_angle == STOP) { // if server wants to stop the car
                print_info();
                update_movements(desired_angle, -2); // stop the car
            } else {
                print_info();
                update_movements(desired_angle, ACCELERATE);
            }
        // }
        client.stop();
        send_coords();
    // }   
    }
}

void send_coords() {
    const uint16_t port = 8888;
    const char * host = "172.20.10.2";
    WiFiClient clientSend;

    int deg_angle = (int) ((dir / M_PI) * 180);
    // Size of array should be 20 bytes (1 float = 8b + 2b for ", " + 1b for '\0')
    // Coordinates must be converted to integers and sent in form: <interaction_index>, <x>, <y>, <deg_angle>
    char coords[33];
    sprintf(coords, "%d, %d, %d, %d", interaction_index, (int) coord_x, (int) coord_y, deg_angle);

    // print_info();
    
    boolean notsent = true;
    while(notsent) { // make sure to keep trying if the connection failed
        if (clientSend.connect(host, port)) //Try to connect to TCP Server
        {
            // clientSend.write(coords);
            Serial.println("sent packet ... ");
            notsent = false;
        } 
        else
        {
            Serial.println("connection failed ... ");
        } 
    }
}

void print_info(void) {

    double absolute_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
    printf("\nVelocity(x, y) | absolute = (%lf, %lf) | %lf\n", velocity_x, velocity_y, absolute_velocity);
    printf("Pos(x, y) = (%lf, %lf)\n", coord_x, coord_y);
    printf("Orientation = %lf\n\n", (dir/M_PI) * 180);

}

/*
* @param desired_angle between MIN_ORIENTATION and MAX_ORIENTATION
* @param desired_accel either -2 (full stop), -1 (slow down), 0 (maintain velocity) or 1 (accelerate)
* Updates the car's coordinate approximation according to the desired parameters
*/
void update_movements(int desired_angle, int desired_accel) {

    if(desired_angle < (MIN_ORIENTATION/M_PI)*180 || desired_angle > (MAX_ORIENTATION/M_PI)*180 
        || desired_accel < -2 || desired_accel > 1) {
        printf("Bad parameters\n");
        return;
    }

    // Current orientation in degrees
    double deg_dir = (dir / M_PI) * 180;
    // Update current orientation
    if(gt(deg_dir, desired_angle)) {
        dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
    } else if(lt(deg_dir, desired_angle)) {
        dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);
    } 

    // Current total velocity (along x and y)
    double curr_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);

    // Movement logic
    if(desired_accel == -2) {
        
        // Stop

        // Assume that stopping is so quick that the deceleration can be assumed constant
        double stop_accel = curr_velocity > 0 ? STOP_DECEL : 0;
        acc_x = - stop_accel * cos(dir);
        acc_y = - stop_accel * sin(dir);
        // Update velocity
        double stop_velocity = fmax(0, curr_velocity - stop_accel);
        velocity_x = stop_velocity * cos(dir);
        velocity_y = stop_velocity * sin(dir);

    } else if(desired_accel == -1) {

        // Slow down (for a corner for example)

        // Assume that we slow down at a constant pace
        double slowdown_accel = curr_velocity > 0 ? -SLOWDOWN_DECEL : 0;
        acc_x = - slowdown_accel * cos(dir);
        acc_y = - slowdown_accel * sin(dir);
        // Update velocity
        double slowdown_velocity = fmax(0, curr_velocity - slowdown_accel);
        velocity_x = slowdown_velocity * cos(dir);
        velocity_y = slowdown_velocity * sin(dir);

    } else if(desired_accel == 0) {

        // Maintain current velocity
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    } else if(desired_accel == 1) {

        // Accelerate
        double acc = fmin(MAX_ACC, (MAX_VELOCITY - curr_velocity) * ACC_UNIT);
        acc_x = acc * cos(dir);
        acc_y = acc * sin(dir); 

        // Update total velocity
        double new_velocity = fmin(MAX_VELOCITY, curr_velocity + acc);

        // Update x/y velocity
        velocity_x = new_velocity * cos(dir);
        velocity_y = new_velocity * sin(dir);

    }

    // Update coordinates
    coord_x += velocity_x;
    coord_y += velocity_y;
}

// if angle > desired_angle
int gt(double angle, int desired_angle) {
    return (angle - desired_angle > ANGLE_PRECISION); 
}

// if angle < desired_angle
int lt(double angle, int desired_angle) {
    return (angle - desired_angle < -ANGLE_PRECISION);
}

// if angle =~ desired_angle
int eq(double angle, int desired_angle) {
    return (fabs(angle - desired_angle) < ANGLE_PRECISION);
}
