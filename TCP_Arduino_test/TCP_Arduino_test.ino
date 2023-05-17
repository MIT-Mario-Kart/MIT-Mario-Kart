#include <ESP8266WiFi.h>

const char* ssid = "Rok's iPhone";       // your network SSID (name)
const char* password = "babalilo";       // your network password

const char* serverAddress = "172.20.10.2";   // server address
const int serverPort = 8998;                   // server port

void setup() {
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
  // Connect to the server
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    Serial.println("Connected to server.");
    
    // Send data to the server
    client.write("CAR1\n20, 20, 180\n");
    Serial.println("Sent data to server.");

    // Wait for a response from the server
    while (client.connected()) {
      if (client.available()) {
        // Read data from the server
        String data = client.readStringUntil('\n');
        Serial.print("Received data: ");
        Serial.println(data);
        // Close the connection
        client.stop();
        Serial.println("Disconnected from server.");
      }
    }

  } else {
    Serial.println("Connection to server failed.");
  }

  // Wait for a few seconds before sending another request
  // delay(1000);
}