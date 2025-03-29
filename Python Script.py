import serial
import time
import joblib  # Assuming the ML model was saved using joblib
import numpy as np

# Load your trained ML model (replace 'model.pkl' with the actual path to your model)
ml_model = joblib.load('model.pkl')  # Ensure you have your model file

# Function to check if the user is authorized based on the model
def is_authorized(voice_features):
    # Assuming 'voice_features' is a list/array of features extracted from the user's voice
    prediction = ml_model.predict(np.array([voice_features]))  # Adjust based on your model
    return prediction == 1  # Assuming 1 means authorized, 0 means unauthorized

# Set up the Bluetooth communication with the same baud rate (9600) as in the Arduino code
bt_serial = serial.Serial('COM5', 9600)  # Replace 'COM5' with the correct port where your Bluetooth module is connected
time.sleep(2)  # Wait for the connection to be established

# Function to send a command to the Arduino via Bluetooth
def send_command(command):
    print(f"Sending command: {command}")
    bt_serial.write((command + '\n').encode())  # Send the command with a newline character
    time.sleep(1)  # Wait for the Arduino to process the command
    response = bt_serial.readline().decode('utf-8').strip()  # Read the response from the Arduino
    print(f"Arduino response: {response}")

# Example voice features (replace this with actual feature extraction logic from your voice input)
voice_features = [0.8, 0.6, 0.7, 0.9]  # Example features, replace with actual extracted data

# Check if the user is authorized before sending commands
if is_authorized(voice_features):
    print("User is authorized. Sending commands to Arduino.")
    
    # Example commands
    commands = [
        "Light 1 On", 
        "Light 1 Off", 
        "Light 2 ON", 
        "Light 2 OFF", 
        "Both Lights On", 
        "Both Lights Off"
    ]

    # Send commands in sequence
    for command in commands:
        send_command(command)
else:
    print("User is NOT authorized. No commands will be sent.")

# Close the Bluetooth serial connection
bt_serial.close()
