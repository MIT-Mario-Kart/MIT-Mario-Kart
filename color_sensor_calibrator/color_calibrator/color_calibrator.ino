#include <math.h>
#define noPaverageseInterrupts 1
// Assignment of the sensor pins
#define S0 5
#define S1 6
#define S2 7
#define S3 8
#define sensorOut 4
/*Calibration values (must be updated before updated before each use)*/
int redMin = 0;
int redMax = 1;
int greenMin = 0;
int greenMax = 1;
int blueMin = 0;
int blueMax = 1;
int redColor = 0;
int greenColor = 0;
int blueColor = 0;
int redFrequency = 0;
int redEdgeTime = 0;
int greenFrequency = 0;
int greenEdgeTime = 0;
int blueFrequency = 0;
int blueEdgeTime = 0;
void setup()
{
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
  Serial.begin(9600);
}
//Initialization of the loop
void loop() {
Serial.println("------------------------------");
{
/*Determination of the photodiode type during measurement
  S2/S3
  LOW/LOW=RED, LOW/HIGH=BLUE,
  HIGH/HIGH=GREEN, HIGH/LOW=CLEAR*/
digitalWrite(S2, LOW);
digitalWrite(S3, LOW);
 
  /*Frequency measurement of the specified color and its as- signment to an RGB value between 0-255*/
float(redEdgeTime) = pulseIn(sensorOut, HIGH) + pulseIn (sensorOut, LOW);
float(redFrequency) = (1 / (redEdgeTime / 1000000)); redColor = map(redFrequency, redMax, redMin, 255, 0); if (redColor > 255) {
      redColor = 255;
    }
    if (redColor < 0) {
      redColor = 0;
}
    /*Output of frequency mapped to 0-255*/
    Serial.print("Red Frequency: ");
    Serial.println(redFrequency);
    Serial.print("R = ");
    Serial.println(redColor);
    delay(100);
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
    Serial.print("Green Frequency: ");
    Serial.println(greenFrequency);
    Serial.print("G = ");
    Serial.println(greenColor);
    delay(100);
}
{
digitalWrite(S2, LOW);
digitalWrite(S3, HIGH);
/*Frequency measurement of the specified color and its as-
signment to an RGB value between 0-255*/
float(blueEdgeTime) = pulseIn(sensorOut, HIGH) + pulseIn (sensorOut, LOW);
float(blueFrequency) = (1 / (blueEdgeTime / 1000000)); blueColor = map(blueFrequency, blueMax, blueMin, 255, 0); if (blueColor > 255) {
      blueColor = 255;
    }
    if (blueColor < 0) {
      blueColor = 0;
}
    /*Output of frequency mapped to 0-255*/
    Serial.print("Blue Frequency: ");
    Serial.println(blueFrequency);
    Serial.print("B = ");
    Serial.println(blueColor);
 
delay(100);
  }
Serial.println("------------------------------"); delay(100);
/*Determination of the measured color by comparison with the values of the other measured colors*/
if (redColor > greenColor and redColor > blueColor) {
Serial.println("Red detected ");
    delay(100);
  }
if (greenColor > redColor and greenColor > blueColor) { Serial.println("Green detected ");
delay(100);
}
if (blueColor > redColor and blueColor > greenColor) { Serial.println("Blue detected ");
delay(100);
}
if (blueColor > 0 and greenColor > 0 and redColor > 0) { Serial.println("Please place an Object in front of the
Sensor");
    delay(100);
}
Serial.println("------------------------------");
  delay(1000);
}
 