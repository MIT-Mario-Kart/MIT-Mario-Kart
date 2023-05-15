#include <ESP8266WiFi.h>
#include <Servo.h>

// Pins
#define PIN_FORWARD 12 // D6 (D2 = 4)
#define PIN_REVERSE 13 //D7 (D1 = 5)
#define SERVO_PIN 15

#define CAR_ID "CAR_ID_TEST"

// Connection constants
const char* ssid = "albert";       // your network SSID (name)
const char* password = "aaaabbbb";       // your network password
const char* serverAddress = "172.20.10.6";   // server address
const int serverPort = 3333;                   // server port

// Global variables
Servo myservo;
double speed_percentage = 1;
int dir = 0;

void setup() {

  // Pin stuff
  pinMode(PIN_FORWARD,OUTPUT); // D6 F (project)
  pinMode(PIN_REVERSE,OUTPUT); // D7 R (project)
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
  Serial.println(WiFi.localIp());
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

        // For now the car moves forward all the time
        analogWrite(PIN_FORWARD, 120);
        digitalWrite(PIN_REVERSE, LOW);

      }
    }

  } else {

    digitalWrite(PIN_FORWARD, LOW);
    digitalWrite(PIN_REVERSE, LOW);
    Serial.println("Connection to server failed.");
  }
}