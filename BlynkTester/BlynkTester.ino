/*New blynk app project
   Home Page
*/

//Include the library files
#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Servo.h>


#define BLYNK_TEMPLATE_ID "TMPLrlGB80Hg"
#define BLYNK_TEMPLATE_NAME "mit"
#define BLYNK_AUTH_TOKEN "rQVPqMJjQ-4KFFi1-0bVdUhvvgOUPdrV"

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "Dan the Pol";//Enter your WIFI name
char pass[] = "RETR0ProkT765";//Enter your WIFI password
Servo myservo;
//Get the button value
BLYNK_WRITE(V0) {
  digitalWrite(6, param.asInt());
}
BLYNK_WRITE(V1) {
  digitalWrite(7, param.asInt());
}
BLYNK_WRITE(V2) {
  myservo.write(180-param.asInt());
}



void setup() {
  //Set the LED pin as an output pin
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  myservo.attach(15);

  //Initialize the Blynk library
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
}

void loop() {
  //Run the Blynk library
  Blynk.run();
}