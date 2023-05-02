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
#define STASSID "Rok's iPhone"
#define STAPSK "babalilo"
#endif

#define UDP_SERVER_IP "10.172.10.2"
#define UDP_PORT 8888

#define START_X 0
#define START_Y 0
#define START_ORIENTATION M_PI/2          // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100               // ~ 1.8 deg
#define MAX_ORIENTATION M_PI
#define MIN_ORIENTATION -MAX_ORIENTATION // -180 deg <= orientation <= 180 deg
#define VELOCITY_UNIT 0.1
#define SLOWDOWN_VELOCITY_UNIT 0.3
#define MAX_VELOCITY 2
#define ANGLE_PRECISION 0.75

#define STOP -1

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
    update_movements(desired_angle);

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

void update_movements(int desired_angle) {

    if(desired_angle == STOP) {
        // Stop
        velocity_x = fmax(0, velocity_x - SLOWDOWN_VELOCITY_UNIT);
        velocity_y = fmax(0, velocity_y - SLOWDOWN_VELOCITY_UNIT);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW);

    } else {

        double deg_dir = (dir / M_PI) * 180;
          
        // Assume moving forwards for now
        if(gt(deg_dir, desired_angle)) {
            dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
        } else if(lt(deg_dir, desired_angle)) {
            dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);
        } 

        velocity_x = fmin(MAX_VELOCITY, velocity_x + cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y + sin(dir));

        digitalWrite(4, HIGH);
        digitalWrite(5, LOW);
        myservo.write(desired_angle);
    }

    coord_x += velocity_x;
    coord_y += velocity_y;

    ++interaction_index;
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