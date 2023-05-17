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
#define CAR_ID_RESET "CAR_ID_RESET"
#define CAR_ID_PU "CAR_ID_PU"

// Connection constants
const char* ssid = "Arthur";       // your network SSID (name)
const char* password = "testtest";       // your network password
const char* serverAddress = "172.20.10.4";   // server address
const int serverPort = 8893;                   // server port

WiFiServer ardServer(9999);
WiFiClient client;

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
const long int PU_MAX = 5000;
long int puDelay = 0;
bool timerStarted = false;
bool sendPu = false;

bool isInMargin(int color, int theorical, int approx){
  int isIn = false;
  if (theorical - approx <= color && color <= theorical + approx){
    isIn = true;
  }
  return isIn;
}

void sendPowUp() {

  char toSend[14];
  // Connect to the server
  Serial.print("CURRENT ZONE / POWERUP SENT : ");
  Serial.print(currZone);
  Serial.print(" / ");
  Serial.println(powerUp);
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    // send 0 or 1 so the server knows when to start the power up code
    sprintf(toSend, "%s\n%d", CAR_ID_PU, powerUp);
    client.write(toSend, 40);
  }
}

void sendReset() {

  // Connect to the server
  
  Serial.print("CURRENT ZONE : ");
  Serial.print(currZone);
  Serial.print(" / ");
  Serial.println("RESET");
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    // send 0 or 1 so the server knows when to start the power up code
    client.write(CAR_ID_RESET);
  }
}

//Calibration values (must be updated before updated before each use)
int redMin = 9174;
int redMax = 33333;
int greenMin = 9615;
int greenMax = 14705;
int blueMin = 12987;
int blueMax = 26315;
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
  digitalWrite(S1, HIGH);

  // Start serial communication for debugging
  Serial.begin(115200);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");
  Serial.println(WiFi.localIP());
  ardServer.begin();
  Serial.println("Server started");
  
}

void loop() {

  String data = "";
   if (!sendPu) {// Connect to the server
    if (timerStarted && ((millis() - puDelay) > PU_MAX)){
          sendReset();
          timerStarted = false;
          puDelay = 0;
          //powerUp = 0;
        }
    else {
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

          while (token != nullptr && count <= 2) {
              if(count == 1) {
                dir = atoi(token);
              } else {
                a = atoi(token);
              }

              // Get the next token
              token = strtok(nullptr, delim);
              ++count;
          }

          // printf("%s\n", data);
          // printf("dir: %d\n", dir);

          myservo.write(dir);
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
            }
          client.stop();
          // Serial.println("Disconnected from server.");
        }
      }
     } else {
          digitalWrite(PIN_FORWARD, LOW);
          digitalWrite(PIN_REVERSE, LOW);
          //Serial.println("Connection to server failed.");
        }
        }} else {
      sendPowUp();
      sendPu = false;
     }
        // For now the car moves forward all the time
        analogWrite(PIN_FORWARD, 120 * speed_percentage * acceleration);
        digitalWrite(PIN_REVERSE, LOW);
     
          // Color sensor =======================================================================================================================================

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
        // Output of frequency mapped to 0-2
        //Serial.print("R = ");
        //Serial.print(redColor);
        //Serial.print(" "); 


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
        //Serial.print("G = ");
        //Serial.print(greenColor);
        //Serial.print(" ");         
        
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
        //Serial.print("B = ");
        //Serial.print(blueColor);
        //Serial.print(" ");

        Serial.println("");

        //Serial.println("-------");

        Serial.print("ACCELERATION : ")
        Serial.println(acceleration);

        
        
        digitalWrite(S2, HIGH);
        digitalWrite(S3, LOW);

        // check if the sensor detects a red tape
        if (isInMargin(redColor, 245, 30) && isInMargin(greenColor, 20, 30) && isInMargin(blueColor, 8, 30)) {
          if (currZone != red){
            currZone = red;
            sendPu = true;
            Serial.println("RED");
          }
        }

        // check if the sensor detects a green tape
        if (isInMargin(redColor, 20, 30) && isInMargin(greenColor, 200, 30) && isInMargin(blueColor, 0, 30)) {
          if (currZone != green){
            currZone = green;
            sendPu = true;
            Serial.println("GREEN");
          }
        }

        // check if the sensor detects a blue tape
        if (isInMargin(redColor, 6, 30) && isInMargin(greenColor, 170, 30) && isInMargin(blueColor, 240, 30)) {
          if (currZone != blue){
            currZone = blue;
            sendPu = true;
            Serial.println("BLUE");
          }
        }  

        // check if the sensor detects a black tape
        if (isInMargin(redColor, 0, 30) && isInMargin(greenColor, 0, 30) && isInMargin(blueColor, 0, 30)) {
          if (powerUp == 0){
            powerUp = 1; // to change back to zero when sent once
            sendPu = true;
            puDelay = millis();
            sendReset();
            timerStarted = true;
            Serial.println("POWER UP");
          }
        }

        // check if the sensor detects the circuit to reset powerup
        if (isInMargin(redColor, 255, 30) && isInMargin(greenColor, 255, 30) && isInMargin(blueColor, 135, 30)) {
          if (powerUp == 1){
              powerUp = 0;
              sendPu = true;
              Serial.println("CIRCUIT");
          } 
        } 
      } 
      