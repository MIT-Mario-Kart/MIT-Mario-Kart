#include <ESP8266WiFi.h>
#include <Servo.h>
#include <dummy.h>
#include <math.h>

// Pins
#define PIN_FORWARD 12 // D6 (D2 = 4)
#define PIN_REVERSE 13 // D7 (D1 = 5)
#define SERVO_PIN 15 // D8

#define CAR_ID "CAR_ID_TEST"
#define CAR_ID_RESET "CAR_ID_RESET"
#define CAR_ID_PU "CAR_ID_PU"

// Connection constants
const char* ssid = "Rok's iPhone";       // your network SSID (name)
const char* password = "babalilo";       // your network password
const char* serverAddress = "172.20.10.2";   // server address
const int serverPort = 8899;                   // server port

WiFiClient client;

const int RED = 2;
const int GREEN = 3;
const int BLUE = 4;

// Global variables
Servo myservo;
double speed_percentage = 1;
int dir = 0;
double received_acc = 1.0;
double acceleration = 1.0;
int currZone = GREEN;

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

void setup() {

  // Pin stuff
  pinMode(PIN_FORWARD,OUTPUT); // D6 F (project)
  pinMode(PIN_REVERSE,OUTPUT); // D7 R (project)
  myservo.attach(SERVO_PIN); // D8 (project)

  // Start serial communication for debugging
  Serial.begin(115200);

  // Connect to Wi-Fi network
  WiFi.onEvent(WiFiEvent); // update connected variable method based on event
  WiFi.mode(WIFI_AP_STA); 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");
  Serial.println(WiFi.localIP()); 
}

void loop() {

  String data = "";
  if (connected) {
     WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
      // Serial.println("Connected to server.");
      
      // Send dummy data
      client.write(CAR_ID);
      // Serial.println("Sent data to server.");

      int a = 1;

      // Wait for a response from the server
      while (client.connected()) {

        if (client.available()) {
          // Read data from the server
          data = client.readStringUntil('\n');
          // Serial.print("Received data: ");
          // Serial.println(data);
          // Close the connection

          char rcvd[data.length()+1];
          data.toCharArray(rcvd, data.length()+1);

          char* token;  // Pointer to the current token
          const char delim[] = " ";  // The delimiter (a space in this case)

          // Use strtok() to separate the string into tokens
          token = strtok(rcvd, delim);

          int count = 1;

          while (token != nullptr && count <= 3) {
              if(count == 1) {
                dir = atoi(token);
              } else if(count == 2) {
                a = atoi(token);
              } else if(count == 3) {
                currZone = atoi(token);
              } else {
                break;
              }

              // Get the next token
              token = strtok(nullptr, delim);
              ++count;
          }

          // printf("%s\n", data);
          // printf("dir: %d\n", dir);
      switch (a) {
        case 0:
            received_acc = 0.8;
            break;
        case 1:
            received_acc = 1.0;
            break;
        case 2:
            received_acc = 1.2;
            break;
        default:
            received_acc = 1.0;
            break;
        }

        switch (currZone) {
            case RED:
                speed_percentage = 0.5;
                break;
            case BLUE:
                speed_percentage = 0.75;
                break;
            case GREEN:
                speed_percentage = 1;
                break;
            default:
                speed_percentage = 1;
                break;
        }
          client.stop();
          // Serial.println("Disconnected from server.");
        }
      }
        myservo.write(dir);
        analogWrite(PIN_FORWARD, 120 * speed_percentage * acceleration);
        digitalWrite(PIN_REVERSE, LOW);
     } else {
          digitalWrite(PIN_FORWARD, LOW);
          digitalWrite(PIN_REVERSE, LOW);
          Serial.println("Connection to server failed.");
        }
    } else {
        digitalWrite(PIN_FORWARD, LOW);
        digitalWrite(PIN_REVERSE, LOW);
        Serial.println("Disconnected from wifi.");
        setup();
    }
}
      
      
