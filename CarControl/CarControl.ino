#include <ESP8266WiFi.h>
#include <Servo.h>

// Pins
#define PIN_D2_FORWARD 4
#define PIN_D1_REVERSE 5
#define SERVO_PIN 15

#define CAR_ID "CAR_ID_TEST"

// Connection constants
const char* ssid = "Rok's iPhone";       // your network SSID (name)
const char* password = "babalilo";       // your network password
const char* serverAddress = "172.20.10.2";   // server address
const int serverPort = 8888;                   // server port

// Global variables
Servo myservo;
double speed_percentage = 1;
int dir = 0;

void setup() {

  // Pin stuff
  pinMode(PIN_D2_FORWARD,OUTPUT); // D6 F (project)
  pinMode(PIN_D1_REVERSE,OUTPUT); // D7 R (project)
  myservo.attach(SERVO_PIN); // D8 (project)


  // Start serial communication for debugging
  Serial.begin(115200);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");
}

void loop() {

  String data = "";

  // Connect to the server
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    // Serial.println("Connected to server.");
    
    // Send dummy data
    client.write(CAR_ID);
    // Serial.println("Sent data to server.");

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
        dir = atoi(rcvd);
        

        printf("%s\n", data);

        printf("dir: %d\n", dir);

        myservo.write(dir);

        client.stop();
        // Serial.println("Disconnected from server.");
      }
    }

  } else {
    Serial.println("Connection to server failed.");
  }
}