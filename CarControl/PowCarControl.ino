#include <ESP8266WiFi.h>
#include <Servo.h>
#include <dummy.h>
#include <math.h>

// Pins
#define PIN_FORWARD 12 // D6 (D2 = 4)
#define PIN_REVERSE 13 // D7 (D1 = 5)
#define SERVO_PIN 15 // D8

// Assignment of the sensor pins
#define S0 5 // D1 or 12
#define S1 4 // D2 or 2
#define S2 0 // D3 or 14
#define S3 2 // D4 or 15
#define sensorOut 16 // D0 or13

#define CAR_ID "CAR_ID_TEST"

// Connection constants
const char* ssid = "S21Babou";       // your network SSID (name)
const char* password = "sltcbabou";       // your network password
const char* serverAddress = "172.20.10.2";   // server address
const int serverPort = 8899;                   // server port

WiFiServer ardServer(9999);
Wificlient client;

// Global variables
Servo myservo;
double speed_percentage = 1;
int dir = 0;

enum Zone {
  red,
  green,
  blue,
};

Zone currZone = green;

int powerUp = 0;
double acceleration = 1.0;

bool isInMargin(int color, int theorical, int approx){
  int isIn = false;
  if (theorical - approx <= color && color <= theorical + approx){
    isIn = true;
  }
  return isIn;
}

char toSend[40]

//Calibration values (must be updated before updated before each use)
int redMin = 19285.71;
int redMax = 62500.00;
int greenMin = 16949.15;
int greenMax = 31250.00;
int blueMin = 20408.16;
int blueMax = 35714.29;
int redColor = 0;
int greenColor = 0;
int blueColor = 0;
int redFrequency = 0;
int redEdgeTime = 0;
int greenFrequency = 0;
int greenEdgeTime = 0;
int blueFrequency = 0;
int blueEdgeTime = 0;
int sensorFrequency = 0;
int sensorEdgeTime = 0;

// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0; 
// Define timeout time in milliseconds (example: 2000ms = 2s)
const long timeoutTime = 2000;

void setup() {

  // Pin stuff
  pinMode(PIN_FORWARD,OUTPUT); // D6 F (project)
  pinMode(PIN_REVERSE,OUTPUT); // D7 R (project)
  myservo.attach(SERVO_PIN); // D8 (project)

  /*definition of the sensor pins*/
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);

  /*Scaling the output frequency
  S0/S1
  LOW/LOW=AUS, LOW/HIGH=2%,
  HIGH/LOW=20%, HIGH/HIGH=100%*/
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);

  // Start serial communication for debugging
  Serial.begin(115200);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");
  ardServer.begin();
  Serial.println("Server started on port 8888");
}

void loop() {

  if (!client.connected()) {
      client = ardServer.available();
  } else{
      if (client.available()) {
        String data = "";

        // Read data from the server
        data = client.readStringUntil('\n');
        // Serial.print("Received data: ");
        // Serial.println(data);
        // Close the connection

        char rcvd[data.length()+1];
        data.toCharArray(rcvd, data.length()+1);

        int originalSize = sizeof(data) / sizeof(data[0]);
        char direction[originalSize - 1];

        for (int i = 0; i < originalSize - 1; i++) {
            direction[i] = data[i];
        }

        double a = data[-1];
        dir = atoi(direction);
        

        printf("%s\n", data);

        printf("dir: %d\n", dir);

        myservo.write(dir);

        client.stop(); // why?

        // Serial.println("Disconnected from server.");

        switch (a) {
            case 0:
                acceleration = 0.8;
                break;
            case 1:
                acceleration = 1.0;
                break;
            case 2:
                acceleration = 1.2;
                break;
            default:
                acceleration = 1.0;
                break;
        }

        switch (currZone) {
            case red:
                speed_percentage = 0.5;
                break;
            case green:
                speed_percentage = 0.75;
                break;
            case blue:
                speed_percentage = 1;
                break;
            default:
                speed_percentage = 1;
                break;


        // For now the car moves forward all the time
        analogWrite(PIN_FORWARD, 120 * speed_percentage * acceleration);
        digitalWrite(PIN_REVERSE, LOW);
        }
      }
  }   
// Color sensor =======================================================================================================================================

        {
        /*Determination of the photodiode type during measurement
          S2/S3
          LOW/LOW=RED, LOW/HIGH=BLUE,
          HIGH/HIGH=GREEN, HIGH/LOW=CLEAR*/
        digitalWrite(S2, LOW);
        digitalWrite(S3, LOW);
        
          /*Frequency measurement of the specified color and its as- signment to an RGB value between 0-255*/
        float(redEdgeTime) = pulseIn(sensorOut, HIGH) + pulseIn (sensorOut, LOW);
        float(redFrequency) = (1 / (redEdgeTime / 1000000)); redColor = map(redFrequency, redMax, redMin, 255, 0); 
            if (redColor > 255) {
              redColor = 255;
            }
            if (redColor < 0) {
              redColor = 0;
            }
            /*Output of frequency mapped to 0-255*/
            Serial.print("R = ");
            Serial.print(redColor);
            Serial.print(" ");


        }
        {
        digitalWrite(S2, HIGH);
        digitalWrite(S3, HIGH);
        /*Frequency measurement of the specified color and its as-
        signment to an RGB value between 0-255*/
        float(greenEdgeTime) = pulseIn(sensorOut, HIGH) + pulseIn (sensorOut, LOW);
        float(greenFrequency) = (1 / (greenEdgeTime / 1000000));
        greenColor = map(greenFrequency, greenMax, greenMin, 255, 0);
            if (greenColor > 255) {
              greenColor = 255;
            }
            if (greenColor < 0) {
              greenColor = 0;
            }
            /*Output of frequency mapped to 0-255*/
            Serial.print("G = ");
            Serial.print(greenColor);
            Serial.print(" ");
        }
        {
        digitalWrite(S2, LOW);
        digitalWrite(S3, HIGH);
        /*Frequency measurement of the specified color and its as-
        signment to an RGB value between 0-255*/
        float(blueEdgeTime) = pulseIn(sensorOut, HIGH) + pulseIn (sensorOut, LOW);
        float(blueFrequency) = (1 / (blueEdgeTime / 1000000)); blueColor = map(blueFrequency, blueMax, blueMin, 255, 0); 
            if (blueColor > 255) {
              blueColor = 255;
            }
            if (blueColor < 0) {
              blueColor = 0;
            }
            /*Output of frequency mapped to 0-255*/
            Serial.print("B = ");
            Serial.print(blueColor);
            Serial.print(" ");

            Serial.println("");

        }
        {
        digitalWrite(S2, HIGH);
        digitalWrite(S3, LOW);

          // check if the sensor detects a red tape
          if (isInMargin(redColor, 255, 30) && isInMargin(greenColor, 55, 30) && isInMargin(blueColor, 80, 30)) {
            if (currZone != red){
              currZone = red;
              sendPowUp();
            }
          }

          // check if the sensor detects a green tape
          if (isInMargin(redColor, 50, 30) && isInMargin(greenColor, 125, 30) && isInMargin(blueColor, 30, 30)) {
            if (currZone != green){
              currZone = green;
              sendPowUp();
            }
          }

          // check if the sensor detects a blue tape
          if (isInMargin(redColor, 35, 30) && isInMargin(greenColor, 130, 30) && isInMargin(blueColor, 255, 30)) {
            if (currZone != blue){
              currZone = blue;
              sendPowUp();
            }
          }  

          // check if the sensor detects a marroon tape
          if (isInMargin(redColor, 150, 30) && isInMargin(greenColor, 20, 30) && isInMargin(blueColor, 20, 30)) {
            if (powerUp == 0){
              powerUp = 1; // to change back to zero when sent once
              sendPowUp();
            }
          }

          // check if the sensor detects the circuit to reset powerup
          if (isInMargin(redColor, 240, 30) && isInMargin(greenColor, 240, 30) && isInMargin(blueColor, 230, 30)) {
            if (powerUp == 1){
                powerUp = 0;
                sendPowUp();
            }
            
          }

  } else {

    digitalWrite(PIN_FORWARD, LOW);
    digitalWrite(PIN_REVERSE, LOW);
    Serial.println("Connection to server failed.");
  }
}

void sendPowUp() {
  // Connect to the server
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    // send 0 or 1 so the server knows when to start the power up code
    sprintf(toSend, "%s\n%d", CAR_ID, powerUp);
    client.write(toSend, 40);
  }
}