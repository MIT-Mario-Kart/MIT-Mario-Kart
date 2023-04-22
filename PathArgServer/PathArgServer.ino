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

#define START_X 0
#define START_Y 0
#define START_ORIENTATION M_PI/2          // 90 deg = facing forwards on trig circle
#define ANGLE_UNIT M_PI/100               // ~ 1.8 deg
#define MAX_ORIENTATION M_PI
#define MIN_ORIENTATION -MAX_ORIENTATION // -180 deg <= orientation <= 180 deg
#define VELOCITY_UNIT 0.1
#define MAX_VELOCITY 2

#define STOP 0
#define FORWARD 1
#define FORWARD_LEFT 2
#define FORWARD_RIGHT 3
#define REVERSE -1
#define REVERSE_LEFT -2
#define REVERSE_RIGHT -3

#define PIN_D2_FORWARD 4
#define PIN_D1_REVERSE 5
#define SERVO_PIN 15

#define DISTANCE 1

void move(void);
void send_coords(void);

const char *ssid = STASSID;
const char *password = STAPSK;

Servo myservo;
ESP8266WebServer server(80);
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

  server.on(("/F"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(90);
    interaction_index += 1;
    handleRoot();
    // No change to dir
    update_movements(FORWARD);
    send_coords();
  });

    server.on(("/FL"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(180);
    interaction_index += 1;
    handleRoot();
    dir += TURNING_ANGLE;
    move_forwards();

    update_movements(FORWARD_LEFT);
    send_coords();
  });

    server.on(("/FR"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(0);
    interaction_index += 1;
    handleRoot();
    dir -= TURNING_ANGLE;
    move_forwards();

    update_movements(FORWARD_RIGHT);
    send_coords();

  });

    server.on(("/B"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(90);
    interaction_index += 1;
    handleRoot();
    // No update to dir
    update_movements(REVERSE);
    send_coords();
  });

    server.on(("/BL"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(180);
    interaction_index += 1;
    handleRoot();
    dir += TURNING_ANGLE;
    move_backwards();

    update_movements(REVERSE_LEFT);
    send_coords();
  });

    server.on(("/BR"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(0);
    interaction_index += 1;
    handleRoot();
    dir -= TURNING_ANGLE;
    move_backwards();

    update_movements(REVERSE_RIGHT);
    send_coords();
  });
  
    server.on(("/S"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    myservo.write(90);
    interaction_index += 1;
    handleRoot();

    update_movements(STOP);
    send_coords();
  });


  server.begin();
  Serial.println("HTTP server started");
  
  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
}



void loop(void) {
  server.handleClient();
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
    if (init_val) {
      SERVER_IP = UDP.remoteIP();
      SERVER_PORT = UDP.remotePort();
      init_val = 1;
    }
  } 
  sendCoords();
}

void send_coords() {

    // Size of array should be 20 bytes (1 float = 8b + 2b for ", " + 1b for '\0')
    char coords[30];
    sprintf(coords, "%d, %f, %f", interaction_index, coord_x, coord_y);
  
    UDP.beginPacket(SERVER_IP, SERVER_PORT); // send ip to server
    UDP.write(coords);
    UDP.endPacket();
}



void update_movements(int next_move_dir) {

    if(FORWARD == next_move_dir) {

        // No orientation update
        velocity_x = fmin(MAX_VELOCITY, velocity_x + VELOCITY_UNIT * cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y + VELOCITY_UNIT * sin(dir));

    } else if(FORWARD_LEFT == next_move_dir) {

        dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);
        velocity_x = fmin(MAX_VELOCITY, velocity_x + VELOCITY_UNIT * cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y + VELOCITY_UNIT * sin(dir));

    } else if(FORWARD_RIGHT == next_move_dir) {

        dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
        velocity_x = fmin(MAX_VELOCITY, velocity_x + VELOCITY_UNIT * cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y + VELOCITY_UNIT * sin(dir));

    } else if(REVERSE == next_move_dir) {

        // No orientation update
        velocity_x = fmin(MAX_VELOCITY, velocity_x + VELOCITY_UNIT * cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y - VELOCITY_UNIT * sin(dir));

    } else if(REVERSE_LEFT == next_move_dir) {

        dir = fmin(MAX_ORIENTATION, dir + ANGLE_UNIT);;
        velocity_x = fmin(MAX_VELOCITY, velocity_x + VELOCITY_UNIT * cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y - VELOCITY_UNIT * sin(dir));

    } else if(REVERSE_RIGHT == next_move_dir) {

        dir = fmax(MIN_ORIENTATION, dir - ANGLE_UNIT);
        velocity_x = fmin(MAX_VELOCITY, velocity_x + VELOCITY_UNIT * cos(dir));
        velocity_y = fmin(MAX_VELOCITY, velocity_y - VELOCITY_UNIT * sin(dir));

    } else if(STOP == next_move_dir) {

        // Assuming that stopping takes ~ 3x less time than accelerating (TODO: calibration)
        velocity_x = fmax(0, velocity_x - 3*VELOCITY_UNIT);
        velocity_y = fmax(0, velocity_y - 3*VELOCITY_UNIT);

        coord_x += velocity_x;
        coord_y += velocity_y;

        return;

    } else {
        Serial.println("Invalid direction\n");
        return;
    }
    
void handleRoot() {
  char* html_body =  
  "  <html> "
 "  <body> "
 "  </body> "

 "  </html>";

  server.send(200, "text/html", html_body);
}

void move_forwards(void) {
    // velocity_x update will be the same for each direction
    velocity_x = fmin(MAX_VELOCITY, velocity_x - VELOCITY_UNIT * sin(dir));
}
