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

#include <iostream>
#include <chrono>

#ifndef STASSID
#define STASSID "Dan the Pol"
#define STAPSK "RETR0ProkT765"
#endif

#define UDP_SERVER_IP "10.172.10.2"
#define UDP_PORT 8888


#define START_ORIENTATION M_PI/2            // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100                 // ~ 1.8 deg
#define MAX_ORIENTATION M_PI
#define MIN_ORIENTATION -MAX_ORIENTATION    // -180 deg <= orientation <= 180 deg
#define ANGLE_PRECISION 1                   // In degrees (if angle is within ± ANGLE_PRECISION 
                                            // it doesn't get updated)
#define MAX_VELOCITY 0.022
#define SLOWDOWN_DECEL STOP_DECEL/2
#define STOP_DECEL MAX_ACC
#define ACC_UNIT MAX_ACC
#define MAX_ACC MAX_VELOCITY

// 1 Unit (along x or y) = 10 cm irl
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
WiFiUDP UDP;

// Pro version
void update_movements(int desired_angle, int desired_accel);

void send_coords(void);
void print_info();
int gt(double angle, int desired_angle);
int lt(double angle, int desired_angle);
int eq(double angle, int desired_angle);

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

double des_dir = 90;
int move = MAINTAIN_VELOCITY;

auto start = std::chrono::high_resolution_clock::now();
ESP8266WebServer server(80);

void setup(void) {
  pinMode(4,OUTPUT); // D2 F
  pinMode(5,OUTPUT); // D1 R
  myservo.attach(15); // D8
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

  server.on(("/F"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(90);
    des_dir = 90;
    move = ACCELERATE;
  });

    server.on(("/FL"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(180);
    des_dir = 135;
    move = ACCELERATE;
  });

    server.on(("/FR"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(0);
    des_dir = 45;
    move = ACCELERATE;
  });

    server.on(("/R"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(90);
    dir = -fabs(dir);
    des_dir = -90;
  });

    server.on(("/RL"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(180);
    dir = -fabs(dir);
    des_dir = -135;
  });

    server.on(("/RR"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(0);
    dir = -fabs(dir);
    des_dir = -45;
  });
  
    server.on(("/S"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    myservo.write(90);
    des_dir = 90;
    move = STOP;
  });

  server.begin();
  Serial.println("HTTP server started");
}


void loop(void) {
  server.handleClient();
  update_movements(des_dir, move);
  if(moving()) print_info();
}

void print_info(void) {

    double total_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
    double total_acc = sqrt(acc_x * acc_x + acc_y * acc_y);
    printf("\nAcceleration(x, y) | absolute = (%lf, %lf) | %lf\n", acc_x, acc_y, total_acc);
    printf("Velocity(x, y) | absolute = (%lf, %lf) | %lf\n", velocity_x, velocity_y, total_velocity);
    printf("Pos(x, y) = (%lf, %lf)\n", coord_x, coord_y);
    printf("Orientation = %lf\n\n", (dir/M_PI) * 180);
    
}

int moving(void) {
  double total_velocity = sqrt(velocity_x * velocity_x + velocity_y * velocity_y);
  double total_acc = sqrt(acc_x * acc_x + acc_y * acc_y);
  return total_velocity > 0 || total_acc > 0; 
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