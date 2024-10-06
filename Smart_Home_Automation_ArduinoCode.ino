#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2, 3); // RX, TX for Bluetooth module

// Pin definitions for devices
const int led1Pin = 9; // First LED
const int led2Pin = 10; // Second LED

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600); // Start Bluetooth communication
  pinMode(led1Pin, OUTPUT); // Set pin modes for devices
  pinMode(led2Pin, OUTPUT);
  
  Serial.println("Smart Home Automation System Ready!");
}

void loop() {
  if (BTSerial.available()) { // Check if there's incoming data from the app
    String command = BTSerial.readStringUntil('\n'); // Read the command until newline

    // Display the command in the Serial Monitor
    Serial.print("Command received: ");
    Serial.println(command);

    // Control devices based on the command
    if (command == "LED1_ON") {
      digitalWrite(led1Pin, HIGH);
      BTSerial.println("LED 1 is ON");
      Serial.println("LED 1 is ON");
    } 
    else if (command == "LED1_OFF") {
      digitalWrite(led1Pin, LOW);
      BTSerial.println("LED 1 is OFF");
      Serial.println("LED 1 is OFF");
    } 
    else if (command == "LED2_ON") {
      digitalWrite(led2Pin, HIGH);
      BTSerial.println("LED 2 is ON");
      Serial.println("LED 2 is ON");
    } 
    else if (command == "LED2_OFF") {
      digitalWrite(led2Pin, LOW);
      BTSerial.println("LED 2 is OFF");
      Serial.println("LED 2 is OFF");
    } 
    else if (command == "Turn on all LEDs") {
      digitalWrite(led1Pin, HIGH);  // Turn on LED 1
      digitalWrite(led2Pin, HIGH);  // Turn on LED 2
      BTSerial.println("All LEDs are ON");
      Serial.println("All LEDs are ON"); 
    }
    else if (command == "turn off all LEDs") {
      digitalWrite(led1Pin, LOW);   // Turn off LED 1
      digitalWrite(led2Pin, LOW);   // Turn off LED 2
      BTSerial.println("All LEDs are OFF"); // Send feedback to the app
      Serial.println("All LEDs are OFF"); 
    }
    else {
      BTSerial.println("Invalid command");
      Serial.println("Invalid command received");
    }
  }
}
