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
#define STASSID "IP"
#define STAPSK "PASS"
#endif

#define UDP_SERVER_IP "10.172.10.2"
#define UDP_PORT 8888

#define START_X 0
#define START_Y 0

#define START_ORIENTATION 0
#define TURNING_ANGLE 0.0873 // ~ 5 degrees
#define ORIENTATION_NAME "ORIENTATION"
#define START_X_NAME "START_X"
#define START_Y_NAME "START_Y"
#define X_NAME "X"
#define Y_NAME "Y"

#define PIN_D2_FORWARD 4
#define PIN_D1_REVERSE 5
#define SERVO_PIN 15

#define FORWARD "/F"
#define REVERSE "/R"
#define FORWARD_LEFT "/FL"
#define FORWARD_RIGHT "/FR"
#define REVERSE_LEFT "/RL"
#define REVERSE_RIGHT "/RR"
#define STOP "/S"

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
float coord_x = START_X;
float coord_y = START_Y;
float dir = START_ORIENTATION;

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
    move_forwards();
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
    send_coords();

  });

    server.on(("/B"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(90);
    interaction_index += 1;
    handleRoot();
    // No update to dir
    move_backwards();
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
    send_coords();
  });
  
    server.on(("/S"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    myservo.write(90);
    interaction_index += 1;
    handleRoot();
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

void sendCoords() {
    UDP.beginPacket(SERVER_IP, SERVER_PORT);//send ip to server
    char coords[sizeof(int)+ 2*sizeof(float) + 5];
    sprintf(coords, "%d, %f, %f", interaction_index, coord_x, coord_y);
    Serial.println(coords);
    UDP.write(coords);
    UDP.endPacket();

    printf("Current coords: %s\n", coords);
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

  coord_x += DISTANCE * cos(dir);
  coord_y += DISTANCE * sin(dir);

}

void move_backwards(void) {

  coord_x += DISTANCE * cos(dir);
  coord_y -= DISTANCE * sin(dir);

}
