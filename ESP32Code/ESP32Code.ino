#include <ESP8266WiFi.h>
#include <Servo.h>
#include <dummy.h>
#include <math.h>

// Assignment of the sensor pins
#define S0 12 // D1 or 12
#define S1 2 // D2 or 2
#define S2 14 // D3 or 14
#define S3 15 // D4 or 15
#define sensorOut 13 // D0 or13

#define CAR_ID_RESET "CAR_ID_RESET"
#define CAR_ID_PU "CAR_ID_PU"

// Connection constants
const char* ssid = "Rok's iPhone";       // your network SSID (name)
const char* password = "babalilo";       // your network password
const char* serverAddress = "172.20.10.2";   // server address
const int serverPort = 8899;                   // server port

const int RED = 2;
const int GREEN = 3;
const int BLUE = 4;

WiFiClient client;

enum Zone {
  red,
  green,
  blue,
};

Zone currZone = green;

int powerUp = 0;
const long int PU_MAX = 5000;
long int puDelay = 0;
bool timerStarted = false;


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
  Serial.print(currZone);
  Serial.print(" : ");
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
  Serial.print(currZone);
  Serial.print(" : ");
  Serial.println("RESET");
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    // send 0 or 1 so the server knows when to start the power up code
    client.write(CAR_ID_RESET);
  }
}

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

void setup() {

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

  
}

void loop() {

  String data = "";

    if (timerStarted && ((millis() - puDelay) > PU_MAX)){
          sendReset();
          timerStarted = false;
          puDelay = 0;
          //powerUp = 0;
        }

     
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
          Serial.print("R -0");
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
          Serial.print("G -0");
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
          Serial.print("B -0");
          blueColor = 0;
        }
        /*Output of frequency mapped to 0-255*/
        //Serial.print("B = ");
        //Serial.print(blueColor);
        //Serial.print(" ");

        Serial.println("");

        //Serial.println("-------");
        
        digitalWrite(S2, HIGH);
        digitalWrite(S3, LOW);

        // check if the sensor detects a red tape
        if (isInMargin(redColor, 83, 30) && isInMargin(greenColor, 0, 30) && isInMargin(blueColor, 0, 30)) {
          if (currZone != red){
            currZone = red;
            powerUp = RED;
            sendPowUp();
            Serial.println("RED");
          }
        }

        // check if the sensor detects a green tape
        if (isInMargin(redColor, 0, 30) && isInMargin(greenColor, 0, 30) && isInMargin(blueColor, 0, 30)) {
          if (currZone != green){
            currZone = green;
            powerUp = GREEN;
            sendPowUp();
            Serial.println("GREEN");
          }
        }

        // check if the sensor detects a blue tape
        if (isInMargin(redColor, 0, 30) && isInMargin(greenColor, 0, 30) && isInMargin(blueColor, 123, 30)) {
          if (currZone != blue){
            currZone = blue;
            powerUp = BLUE;
            sendPowUp();
            Serial.println("BLUE");
          }
        }  

        // check if the sensor detects a white tape
        if (isInMargin(redColor, 255, 30) && isInMargin(greenColor, 255, 30) && isInMargin(blueColor, 255, 30)) {
          if (powerUp == 0){
            powerUp = 1; // to change back to zero when sent once
            sendPowUp();
            puDelay = millis();
            sendReset();
            timerStarted = true;
            Serial.println("POWER UP");
          }
        }

        // check if the sensor detects the circuit to reset powerup
        if (isInMargin(redColor, 97, 30) && isInMargin(greenColor, 86, 30) && isInMargin(blueColor, 0, 30)) {
          if (powerUp == 1){
              powerUp = 0;
              sendPowUp();
              Serial.println("CIRCUIT");
          } 
        }
} 
      
      
