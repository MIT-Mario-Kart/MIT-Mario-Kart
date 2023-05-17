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

#define SERVER_IP "172.20.10.2"
#define SERVER_PORT 8998

#define ID "CAR1"

#define START_ORIENTATION 270
#define ANGLE_UNIT M_PI/1000                // ~ 0.18 deg
#define SERVO_SPEED 1                       // How many degrees the servo turns in one iteration
#define MAX_ORIENTATION 2*M_PI              // 0 deg <= orientation <= 360 deg
#define MIN_ORIENTATION 0                   
#define ANGLE_PRECISION 3                   // In degrees (if angle is within ± ANGLE_PRECISION 
                                            // it doesn't get updated)
#define MAX_VELOCITY 0.25
#define GREEN_V MAX_VELOCITY
#define BLUE_V MAX_VELOCITY*0.7
#define RED_V MAX_VELOCITY*0.3

#define MAX_ACC 0.25
#define STOP_DECEL MAX_ACC
#define ACC_UNIT MAX_ACC

#define START_X 20
#define START_Y 20

#define STOP -1
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

// Using doubles for extra precision (lol)
double coord_x = START_X;
double coord_y = START_Y;
double dir = (START_ORIENTATION/180)*M_PI;
int desired_orientation = START_ORIENTATION;
int desired_move = STOP;
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
  WiFi.mode(WIFI_AP_STA); 
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
        desired_move = STOP; // STOP the car 
        setup();
    } else {
      send_coords();
      desired_move = ACCELERATE;
    }

  update_movements();
  print_info();
}

void send_coords() {

  // Connect to the server
  WiFiClient client;
  const char* serverAddress = SERVER_IP;   // server address

  if (client.connect(serverAddress, SERVER_PORT)) {
    // Serial.println("Connected to server.");

    int deg_angle = (int) ((dir / M_PI) * 180.0);
    // Size of array should be 20 bytes (1 float = 8b + 2b for ", " + 1b for '\0')
    // Coordinates must be converted to integers and sent in form: 
    // ID
    // <x>, <y>, <deg_angle>
    char coords[33];
    int len = sprintf(coords, ID"\n%d, %d, %d\n", (int) coord_x, (int) coord_y, deg_angle);
    
    // Send data to the server
    if(client.write(coords) != len) {
      Serial.println("Error when sending packet");
    } else {
      // Serial.println("Sent data to server.");
    }

    // Wait for a response from the server
    while (client.connected()) {
      if (client.available()) {
        // Read data from the server
        String data = client.readStringUntil('\n');
        // Serial.print("Received data: ");
        // Serial.println(data);
        char rcvd[data.length()];
        data.toCharArray(rcvd, data.length());
        dir = atoi(rcvd);
        // Close the connection
        client.stop();
        // Serial.println("Disconnected from server.");
        break;
      }
    }
  } else {
    Serial.println("Connection to server failed.");
  }

    // const uint16_t port = 8998;
    // const char * host = "172.20.10.4";
    // WiFiClient clientSend;

    // int deg_angle = (int) ((dir / M_PI) * 180);
    // // Size of array should be 20 bytes (1 float = 8b + 2b for ", " + 1b for '\0')
    // // Coordinates must be converted to integers and sent in form: 
    // // ID
    // // <x>, <y>, <deg_angle>
    // char coords[33];
    // sprintf(coords, ID"\n%d, %d, %d", (int) coord_x, (int) coord_y, deg_angle);

    // // print_info();
    
    // boolean notsent = true;
    // while(notsent) { // make sure to keep trying if the connection failed
    //     if (clientSend.connect(host, port)) //Try to connect to TCP Server
    //     {
    //         clientSend.write(coords);
    //         // Serial.println("sent packet ... ");
    //         notsent = false;
    //     } 
    //     else
    //     {
    //         Serial.println("connection failed ... ");
    //     } 
    // }
}











void print_info(void) {

    double absolute_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
    printf("\nVelocity(x, y) | absolute = (%lf, %lf) | %lf\n", velocity_x, velocity_y, absolute_velocity);
    printf("Pos(x, y) = (%lf, %lf)\n", coord_x, coord_y);
    printf("Orientation = %lf\n\n", (dir/M_PI) * 180.0);

}

/*
* @param desired_angle between MIN_ORIENTATION and MAX_ORIENTATION
* @param desired_accel either -1 (slow down), 0 (maintain velocity) or 1 (accelerate)
* Updates the car's coordinate approximation according to the desired parameters
*/
void update_movements() {

    // Current orientation in degrees
    int deg_dir = (int) ((dir / M_PI) * 180.0);

    int diff = abs(deg_dir - abs(desired_orientation));
    // Update current orientation
    if(gt((double) diff, 0)) {
        if(desired_orientation < 0) deg_dir = modulo(deg_dir - ((int) ((ANGLE_UNIT/M_PI)*180.0)), 360);
        if(desired_orientation > 0) deg_dir = modulo(deg_dir + ((int) ((ANGLE_UNIT/M_PI)*180.0)), 360);
        dir = (deg_dir/180.0)*M_PI;
    } 

    // Current total acceleration
    double curr_acc = sqrt(acc_x * acc_x + acc_y * acc_y);

    // Current total velocity (along x and y)
    double curr_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);

    // Movement logic
    if(desired_move == -1) {
        
        // Slow down

        // Assume that stopping is so quick that the deceleration can be assumed constant
        curr_acc = curr_velocity > 0 ? fmax(-STOP_DECEL, curr_acc - ACC_UNIT) : 0;
        acc_x = curr_acc * cos(dir);
        acc_y = -curr_acc * sin(dir);
        // Update velocity
        curr_velocity = fmax(0, curr_velocity + curr_acc);
        velocity_x = curr_velocity * cos(dir);
        velocity_y = -curr_velocity * sin(dir);

    } else if(desired_move == 0) {

        // Maintain speed

        // Don't change total acceleration, update for orientation
        acc_x = curr_acc * cos(dir);
        acc_y = -curr_acc * sin(dir);
        // Don't change total velocity, update for orientation
        velocity_x = curr_velocity * cos(dir);
        velocity_y = -curr_velocity * sin(dir);

    } else if(desired_move == 1) {

        // Accelerate 

        // Update acceleration (the higher the speed, the lower the acceleration)
        curr_acc = fmin(MAX_ACC, (MAX_VELOCITY - curr_velocity) * ACC_UNIT);
        acc_x = curr_acc * cos(dir);
        acc_y = -curr_acc * sin(dir); 
        // Update velocity
        curr_velocity = fmin(MAX_VELOCITY, curr_velocity + curr_acc);
        velocity_x = curr_velocity * cos(dir);
        velocity_y = -curr_velocity * sin(dir);

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


int modulo(int nb, int base)
{
    int remainder = nb % base;
    return remainder < 0 ? remainder + base : remainder;
}
