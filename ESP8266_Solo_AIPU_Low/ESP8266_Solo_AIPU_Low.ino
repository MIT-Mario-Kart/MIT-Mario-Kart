#include <ESP8266WiFi.h>
#include <Servo.h>
#include <dummy.h>
#include <math.h>
#include <ESP8266WebServer.h>
#include <cstdlib>

// Pins
#define PIN_FORWARD 12    // D6
#define PIN_REVERSE 13    // D7
#define SERVO_PIN 15      // D8

#define CAR_ID "CAR_ID_TEST"
#define CAR_ID_RESET "CAR_ID_RESET"
#define CAR_ID_PU "CAR_ID_PU"

// Assignment of the sensor pins
#define S0 4            // D2
#define S1 5            // D1
#define S2 0            // D3
#define S3 2            // D4
#define sensorOut 14    // D5

// Connection constants
const char* ssid = "albert";                    // your network SSID (name)
const char* password = "aaaabbbb";              // your network password
const char* serverAddress = "172.20.10.6";      // server address
const int serverPort = 8899;                    // server port

WiFiClient client;

// ------------------- Colour sensor code --------------------
enum Zone {
  red,
  green,
  blue,
};

Zone currZone = green;

//int zoneOrPowUp = 0;
const long int PU_MAX = 5000;
long int puDelay = 0;
bool timerIsStarted = false;

bool isInMargin(int color, int theorical, int approx){
  int isIn = false;
  if (theorical - approx <= color && color <= theorical + approx){
    isIn = true;
  }
  return isIn;
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

const int RED = 2;
const int GREEN = 3;
const int BLUE = 4;
// ---------------------------------------------------------------

// Global variables
Servo myservo;
double speed_percentage = 1;
int dir = 0;
int rcvd_acc = 0;
char toSend[40];


#define PU_NONE 0
#define PU_STOP 1
#define PU_SLOWDOWN 2
#define PU_SPEEDUP 3
// #define PU_INVERT 4

#define SLOWDOWN_PRCNT 0.75
#define SPEEDUP_PRCNT 1.25
#define NORMAL_SPEED 200
int receivedPowerup = PU_NONE;
bool isPowerupd = false;
// bool invertControls = false;

/* void activatePowerup() {

  srand((unsigned) time(NULL));
  // receivedPowerup = (abs(rand()) % 3) + 2;
  receivedPowerup = (abs(rand()) % 2) + 2;

  if(receivedPowerup == PU_SLOWDOWN){
    Serial.println("Slowdown");
  } else if(receivedPowerup == PU_SPEEDUP) {
    Serial.println("Speedup");
  // } else if(receivedPowerup == PU_INVERT) {
  //   Serial.println("Invert");
  } else {
    Serial.println("Error on PU");
  }

} */

void sendPowUp() {
  // Connect to the server
  /* Serial.print(currZone);
  Serial.print(" : ");
  Serial.println(powerUp); */
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    // send 0 or 1 so the server knows when to start the power up code
    sprintf(toSend, "%s\n%d", CAR_ID, powerUp);
    client.write(toSend, 40);
  }
}





void setup() {

  // Pin stuff
  pinMode(PIN_FORWARD,OUTPUT);
  pinMode(PIN_REVERSE,OUTPUT);
  myservo.attach(SERVO_PIN);

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
  Serial.println();

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");
  Serial.println(WiFi.localIP());

  myservo.write(90);
}



void loop() {

   // Reset powerups
  if (timerIsStarted && ((millis() - puDelay) > PU_MAX)) {
    
    timerIsStarted = false;
    puDelay = 0;
    //zoneOrPowUp = currZone + 1;

    // My powerups
    //receivedPowerup = PU_NONE;
    isPowerupd = false;
    // invertControls = false;
    Serial.println("Powerup reset");
  }

  //------------------------------- Colour sensor -------------------------------

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

  digitalWrite(S2, HIGH);
  digitalWrite(S3, LOW);


  if(isInMargin(redColor, 245, 30) && isInMargin(greenColor, 20, 30) && isInMargin(blueColor, 8, 30)) {
    // check if the sensor detects a RED tape
    if (currZone != red){
      currZone = red;

    }
  } else if(isInMargin(redColor, 20, 30) && isInMargin(greenColor, 200, 30) && isInMargin(blueColor, 0, 30)) {
    // check if the sensor detects a GREEN tape
    if (currZone != green){
      currZone = green;

    }
  } else if(isInMargin(redColor, 6, 30) && isInMargin(greenColor, 170, 30) && isInMargin(blueColor, 240, 30)) {
    // check if the sensor detects a BLUE tape
    if (currZone != blue){
      currZone = blue;

    }
  } else if(isInMargin(redColor, 0, 30) && isInMargin(greenColor, 0, 30) && isInMargin(blueColor, 0, 30)) {
    // check if the sensor detects a black tape (POWERUP)
    if (zoneOrPowUp != 1 && !isPowerupd) {
      isPowerupd = true;
      sendPowUp();
      puDelay = millis();
      timerIsStarted = true;
    }
  } else if(isInMargin(redColor, 255, 30) && isInMargin(greenColor, 255, 30) && isInMargin(blueColor, 135, 30)) {
     // check if the sensor detects the CIRCUIT to reset powerup
    if (zoneOrPowUp != 0){ 
      Serial.println("Circuit");
    }
  }

  switch (currZone) {
  case red:
    speed_percentage = SLOWDOWN_PRCNT;
    break;

  case blue:
    speed_percentage = 1;
    break;

  case green:
    speed_percentage = SPEEDUP_PRCNT;
    break;
    
  default:
    speed_percentage = 1;
    break;
  }

  // ----------------------------------------------------------------------------

  String data = "";

  // Connect to the server
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

          char* token;  // Pointer to the current token
          const char delim[] = " ";  // The delimiter (a space in this case)

          // Use strtok() to separate the string into tokens
          token = strtok(rcvd, delim);

          int count = 1;

          while (token != nullptr && count <= 2) {
              if(count == 1) {
                dir = atoi(token);
              } else if(count == 2) {
                rcvd_acc = atoi(token);
              } else {
                break;
              }

              // Get the next token
              token = strtok(nullptr, delim);
              ++count;
          }
        
        
        // dir = 200 = stop car
        if (dir == 200) {

          printf("Stop\n");
          rcvd_acc = 0;


        } else if(0 <= dir && dir <= 180) {

          printf("data: %s\n", data);
          printf("dir: %d\n", dir);
          myservo.write(dir);
          // acceleration = 1;

          // Car moves forward all the time unless -1 is sent

        } else {

          printf("Incorrect dir received: %d", dir);
          rcvd_acc = 0;

        }
        client.stop();
        // Serial.println("Disconnected from server.");
      }
    }





  /* if(receivedPowerup == PU_STOP) {

    isPowerupd = false;
    speed_percentage = 0;
    
  //} else if(isPowerupd) {

      // Should be ok]

  } else if(receivedPowerup == PU_SLOWDOWN) {

    isPowerupd = true;
    speed_percentage = SLOWDOWN_PRCNT;

  } else if(receivedPowerup == PU_SPEEDUP) {

    isPowerupd = true;
    speed_percentage = SPEEDUP_PRCNT;

  // } else if(receivedPowerup == PU_INVERT) {

  //   isPowerupd = true;
  //   invertControls = true;

  } else if(receivedPowerup == PU_NONE) {

    speed_percentage = 1;

  } */
  // Controlling motors

  if(rcvd_acc == 0) {
    digitalWrite(PIN_FORWARD, LOW);
    digitalWrite(PIN_REVERSE, LOW);
    

  } else if (rcvd_acc > 0) {

    digitalWrite(PIN_REVERSE, LOW);
    analogWrite(PIN_FORWARD, NORMAL_SPEED * rcvd_acc * speed_percentage);

  } else if(rcvd_acc < 0) {

    digitalWrite(PIN_FORWARD, LOW);
    analogWrite(PIN_REVERSE, NORMAL_SPEED * rcvd_acc * speed_percentage);

  }

  } else {

    digitalWrite(PIN_FORWARD, LOW);
    digitalWrite(PIN_REVERSE, LOW);
    Serial.println("Connection to server failed.");

  }
}