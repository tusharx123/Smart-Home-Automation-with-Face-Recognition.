#include <SoftwareSerial.h>

#define relay1 13    // Relay connected to pin 13

// Create SoftwareSerial object for Bluetooth communication
SoftwareSerial BTSerial(4, 5); // RX on pin 4, TX on pin 5

void setup() {
  BTSerial.begin(9600);  // Start Bluetooth communication at 9600 baud
  Serial.begin(9600);    // Start hardware serial for debugging (USB connection)
  
  pinMode(relay1, OUTPUT); // Set relay pin as output
  digitalWrite(relay1, HIGH); // Switch relay off initially
  
  Serial.println("Smart Home Automation System Ready!");
}

void loop() {
  // Check if there's incoming data from the Bluetooth app
  if (BTSerial.available()) {
    String command = BTSerial.readStringUntil('\n'); // Read the command until newline

    // Display the command in the Serial Monitor
    Serial.print("Command received: ");
    Serial.println(command);

    // Control the bulb based on the command
    if (command == "Light 1 ON") {
      digitalWrite(relay1, LOW); // Turn on the light (relay ON)
      Serial.println("Light is ON");
    } 
    else if (command == "Turn Off Light") {
      digitalWrite(relay1, HIGH); // Turn off the light (relay OFF)
      Serial.println("Light is OFF");
    } 
    else {
      Serial.println("Invalid command received");
    }
  }
}
