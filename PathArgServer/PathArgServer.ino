#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>

#include <uri/UriBraces.h>
#include <uri/UriRegex.h>
#include <Servo.h>

#ifndef STASSID
#define STASSID "IP"
#define STAPSK "PASS"
#endif

#define UDP_SERVER_IP "10.172.10.2"
#define UDP_PORT 8888

#define START_X 0
#define START_Y 0

#define START_ORIENTATION 0
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

const char *ssid = STASSID;
const char *password = STAPSK;

Servo myservo;
ESP8266WebServer server(80);
WiFiUDP UDP;

int coord_x = START_X;
int coord_y = START_Y;
int dir = START_ORIENTATION;

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
    coord_y += DISTANCE;
  });

    server.on(("/FL"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(180);
    coord_x -= DISTANCE;
    coord_y += DISTANCE;
    sendCoords();
  });

    server.on(("/FR"), []() {
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);
    myservo.write(0);
    coord_x += DISTANCE;
    coord_y += DISTANCE;
    sendCoords();

  });

    server.on(("/B"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(90);
    coord_y += DISTANCE;
    sendCoords();
  });

    server.on(("/BL"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(180);
    coord_x -= DISTANCE;
    coord_y -= DISTANCE;
    sendCoords();
  });

    server.on(("/BR"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, HIGH);
    myservo.write(0);
    coord_x += DISTANCE
    coord_y -= DISTANCE;
    sendCoords();
  });
  
    server.on(("/S"), []() {
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    myservo.write(90);
    sendCoords();
  });


  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}

void sendCoords() {
    UDP.beginPacket(UDP_SERVER_IP, UDP_PORT);
    UDP.write("%d, %d", coord_x, coord_y);
    UDP.endPacket();
    }
