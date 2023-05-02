#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>

#include <uri/UriBraces.h>
#include <uri/UriRegex.h>
#include <Servo.h>

#include <math.h>
#include <stdlib.h>

#ifndef STASSID
#define STASSID "Dan the Pol"
#define STAPSK "RETR0ProkT765"
#endif

#define UDP_SERVER_IP "10.172.10.2"
#define UDP_PORT 8888


#define START_ORIENTATION M_PI/2            // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100                 // ~ 1.8 deg
#define MAX_ORIENTATION 2*M_PI
#define MIN_ORIENTATION 0                   // 0 deg <= orientation <= 360 deg
#define ANGLE_PRECISION 1                   // In degrees (if angle is within ± ANGLE_PRECISION 
                                            // it doesn't get updated)
#define MAX_VELOCITY 0.025
#define STOP_DECEL 0.025
#define ACC_UNIT 0.025
#define MAX_ACC 0.025

// 1 Unit (along x or y) =~ 10 cm irl
#define START_X 0   
#define START_Y 0

#define STOP -1
#define MAINTAIN_VELOCITY 0
#define ACCELERATE 1

#define PIN_D2_FORWARD 4
#define PIN_D1_REVERSE 5
#define SERVO_PIN 15

const char *ssid = STASSID;
const char *password = STAPSK;

Servo myservo;
WiFiUDP UDP;

char packet[255];
uint16_t SERVER_PORT;
IPAddress SERVER_IP;
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

void setup(void) {
  pinMode(PIN_D2_FORWARD,OUTPUT); // D2 F
  pinMode(PIN_D1_REVERSE,OUTPUT); // D1 R
  myservo.attach(SERVO_PIN); // D8
  // 172.20.10.5

  Serial.begin(115200);
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

  if (MDNS.begin("esp8266")) { Serial.println("MDNS responder started"); }
  
  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
}

void loop(void) {

  // If packet received...
  int packetSize = UDP.parsePacket();
  if (packetSize) {
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize); 
    int len = UDP.read(packet, 255);
    if (len > 0)
    {
      packet[len] = '\0';
    }
    Serial.print("Packet received: ");
    Serial.println(packet);

    int desired_angle = atoi(packet);
    update_movements(desired_angle, ACCELERATE);

    if (init_val) {
      SERVER_IP = UDP.remoteIP();
      SERVER_PORT = UDP.remotePort();
      init_val = 0;
    }
  } 
  send_coords();
}

void send_coords() { 

    int deg_angle = (int) ((dir / M_PI) * 180);
    // Size of array should be 20 bytes (1 float = 8b + 2b for ", " + 1b for '\0')
    // Coordinates must be converted to integers and sent in form: <interaction_index>, <x>, <y>, <deg_angle>
    char coords[33];
    sprintf(coords, "%d, %d, %d, %d", interaction_index, (int) coord_x, (int) coord_y, deg_angle);

    // print_info();
      

    UDP.beginPacket(SERVER_IP, SERVER_PORT); // send ip to server
    UDP.write(coords);
    UDP.endPacket();
}

void print_info(void) {

    double absolute_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
    printf("\nVelocity(x, y) | absolute = (%lf, %lf) | %lf\n", velocity_x, velocity_y, absolute_velocity);
    printf("Pos(x, y) = (%lf, %lf)\n", coord_x, coord_y);
    printf("Orientation = %lf\n\n", (dir/M_PI) * 180);

}

/*
* @param desired_angle between MIN_ORIENTATION and MAX_ORIENTATION
* @param desired_accel either -1 (slow down), 0 (maintain velocity) or 1 (accelerate)
* Updates the car's coordinate approximation according to the desired parameters
*/
void update_movements(int desired_angle, int desired_accel) {

    if(desired_angle < (MIN_ORIENTATION/M_PI)*180 || desired_angle > (MAX_ORIENTATION/M_PI)*180 
        || desired_accel < -1 || desired_accel > 1) {
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

    // Current total acceleration
    double curr_acc = sqrt(acc_x * acc_x + acc_y * acc_y);

    // Current total velocity (along x and y)
    double curr_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);

    // Movement logic
    if(desired_accel == -1) {
        
        // Slow down

        // Assume that stopping is so quick that the deceleration can be assumed constant
        curr_acc = curr_velocity > 0 ? fmax(-STOP_DECEL, curr_acc - ACC_UNIT) : 0;
        acc_x = curr_acc * cos(dir);
        acc_y = curr_acc * sin(dir);
        // Update velocity
        curr_velocity = fmax(0, curr_velocity + curr_acc);
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    } else if(desired_accel == 0) {

        // Maintain speed

        // Don't change total acceleration, update for orientation
        acc_x = curr_acc * cos(dir);
        acc_y = curr_acc * sin(dir);
        // Don't change total velocity, update for orientation
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

    } else if(desired_accel == 1) {

        // Accelerate 

        // Update acceleration (the higher the speed, the lower the acceleration)
        curr_acc = fmin(MAX_ACC, (MAX_VELOCITY - curr_velocity) * ACC_UNIT);
        acc_x = curr_acc * cos(dir);
        acc_y = curr_acc * sin(dir); 
        // Update velocity
        curr_velocity = fmin(MAX_VELOCITY, curr_velocity + curr_acc);
        velocity_x = curr_velocity * cos(dir);
        velocity_y = curr_velocity * sin(dir);

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