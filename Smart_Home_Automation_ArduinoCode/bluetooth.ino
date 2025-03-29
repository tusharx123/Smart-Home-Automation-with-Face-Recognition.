char val;
String commandLower;

void setup() {
    pinMode(13, OUTPUT);  // Set pin 13 for the bulb (or relay)
    Serial.begin(9600);  // Start the serial communication at 9600 baud
    digitalWrite(13, HIGH);  // Start with the bulb off
}

void loop() {
    if (Serial.available()) {
        val = Serial.read();  // Read the incoming byte

        // Handle tap-based control (when the app sends 1 or 2)
        if (val == '1') {
            digitalWrite(13, LOW);  // Turn on the bulb (1 means ON)
        } 
        else if (val == '2') {
            digitalWrite(13, HIGH); // Turn off the bulb (2 means OFF)
        }

        // Handle voice-based control (when a voice command like "turn on the light" is received)
        // Read the full incoming data
        if (Serial.available()) {
            commandLower = Serial.readString().toLowerCase();  // Read the command and convert it to lowercase

            // Check for the "turn on the light" or "turn off the light" commands
            if (commandLower.indexOf("turn on the light") >= 0) {
                digitalWrite(13, LOW);  // Turn on the bulb
                Serial.println("Light is ON");  // Print status for debugging
            } 
            else if (commandLower.indexOf("turn off the light") >= 0) {
                digitalWrite(13, HIGH); // Turn off the bulb
                Serial.println("Light is OFF");  // Print status for debugging
            }
        }
    }

    delay(100);  // Small delay to avoid too many readings at once
}
