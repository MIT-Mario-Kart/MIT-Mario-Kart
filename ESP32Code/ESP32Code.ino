#include <WiFi.h>
#include <dummy.h>
#include <math.h>
#include <SoftwareSerial.h>



#define RX_PIN 12       // IO12 (green)
#define TX_PIN 13       // IO13 (blue)
#define BAUD_RATE 115200
#define BREAK_CHAR "\n"
SoftwareSerial ESPSerial(RX_PIN, TX_PIN);

#define CAR_ID "CAR_ID_TEST"
#define CAR_ID_RESET "CAR_ID_RESET"
#define CAR_ID_PU "CAR_ID_PU"

// Connection constants
const char* ssid = "Dan the Pol";       // your network SSID (name)
const char* password = "RETR0ProkT765";       // your network password
const char* serverAddress = "172.20.10.5";   // server address
const int serverPort = 8999;                   // server port

WiFiClient client;

void setup() {

  // Start serial communication for debugging
  ESPSerial.begin(115200);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void loop() {

  // Receive from RX (data to be relayed)
  String rcvdRX = CAR_ID;
  rcvdRX.concat(' ');
  if(ESPSerial.available() > 0){
    while(ESPSerial.available()) {
      char next = ESPSerial.read();
      if(next == '\n') {
        break;
      } else {
        rcvdRX.concat(next);
      }
    }
  }
  size_t rsrvlen = rcvdRX.length();
  char relaySRV[rsrvlen + 1];
  rcvdRX.toCharArray(relaySRV, rsrvlen);

  // Connect to the server
  String rcvdSRV = "";
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    
    // Send data to the server
    client.write(relaySRV, rsrvlen);

    // Wait for a response from the server
    while (client.connected()) {
      if (client.available()) {
        // Read data from the server
        rcvdSRV = client.readStringUntil('\n');
        // Close the connection
        client.stop();
      }
    }
  

    // Send over TX (only send over TX if we received something)

    // Add "\n" to received string
    rcvdSRV.concat(BREAK_CHAR);
    size_t rtxlen = rcvdSRV.length();
    // Additional check just in case
    if(rtxlen > 0) {
      char relayTX[rtxlen + 1];
      rcvdSRV.toCharArray(relayTX, rtxlen);
      // Write to TX
      ESPSerial.write(relayTX);
    }
  } 
} 
      
      
