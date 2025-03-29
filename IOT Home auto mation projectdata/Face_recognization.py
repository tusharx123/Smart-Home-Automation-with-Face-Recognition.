# import cv2 as c
# import speech_recognition as sr
# import threading
# import pyttsx3
# import serial
# import time
#
# # Initialize serial communication with Arduino over USB
# arduino = serial.Serial('COM8', 9600)
# time.sleep(2)
#
# # Load trained face recognizer model
# recognize = c.face.LBPHFaceRecognizer.create()
# recognize.read('Trained_model/model.yml')
# faceCascade = c.CascadeClassifier('frontalface.xml')
#
# # Font settings
# font = c.FONT_HERSHEY_SIMPLEX
#
# # Person ID and names list
# names = ['Access', 'Access']
#
# # Open the webcam
# cam = c.VideoCapture(0)
# cam.set(3, 640)
# cam.set(4, 480)
#
# # Minimum size for face detection
# minW = 0.1 * cam.get(3)
# minH = 0.1 * cam.get(4)
#
# # Initialize recognizer for voice commands
# recognizer = sr.Recognizer()
#
# # Lock to prevent multiple voice threads
# voice_command_lock = threading.Lock()
#
# def say(query):
#     """Text-to-speech function."""
#     if query != "none":
#         speaker = pyttsx3.init()
#         voices = speaker.getProperty('voices')
#         speaker.setProperty('voice', voices[0].id)
#         speaker.setProperty('rate', 130)
#         speaker.say(query)
#         speaker.runAndWait()
#
# def send_command_to_arduino(command):
#     """Send command to Arduino."""
#     arduino.write(command.encode())
#
# def listen_for_command():
#     """Listen for voice commands to control the light."""
#     if voice_command_lock.acquire(blocking=False):
#         try:
#             with sr.Microphone() as source:
#                 recognizer.adjust_for_ambient_noise(source)
#                 print("Listening for command...")
#                 say("Listening for command.")
#                 try:
#                     audio = recognizer.listen(source, timeout=10)  # Increase timeout
#                     command_text = recognizer.recognize_google(audio).lower()
#                     print("You said:", command_text)
#
#                     if "turn on light" in command_text:
#                         send_command_to_arduino('1')
#                         say("Turning on the light.")
#                     elif "turn off light" in command_text:
#                         send_command_to_arduino('2')
#                         say("Turning off the light.")
#                     else:
#                         say("Command not recognized.")
#                 except sr.UnknownValueError:
#                     print("Could not understand the audio.")
#                     say("Sorry, I didn't catch that.")
#                 except sr.RequestError as e:
#                     print(f"Error with the speech recognition service: {e}")
#                     say("Speech recognition service is unavailable.")
#         finally:
#             voice_command_lock.release()
#
# # Main loop for face recognition and voice command
# while True:
#     ret, img = cam.read()
#     if not ret:
#         print("Failed to capture image from camera.")
#         break
#
#     convert_img = c.cvtColor(img, c.COLOR_BGR2GRAY)
#     faces = faceCascade.detectMultiScale(convert_img, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))
#
#     for (x, y, z, h) in faces:
#         c.rectangle(img, (x, y), (x + z, y + h), (0, 255, 0), 2)
#         id, accuracy = recognize.predict(convert_img[y:y + h, x:x + z])
#         accuracy_text = f"{round(100 - accuracy)}%"
#
#         if int(100 - accuracy) > 30:
#             id_text = names[id]
#             access_granted = True
#         else:
#             id_text = "Unknown"
#             access_granted = False
#
#         c.putText(img, str(id_text), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
#         c.putText(img, accuracy_text, (x + 5, y + h + 20), font, 1, (255, 255, 255), 1)
#
#         if access_granted:
#             if not threading.active_count() > 1:  # Ensure only one voice thread runs
#                 threading.Thread(target=listen_for_command).start()
#
#     c.imshow('camera', img)
#
#     if c.waitKey(10) & 0xff == 27:  # Press 'ESC' to exit
#         break
#
# # Release resources
# cam.release()
# c.destroyAllWindows()
# arduino.close()

import cv2 as c
import speech_recognition as sr
import threading
import pyttsx3
import serial
import time

# Initialize serial communication with Arduino over USB
arduino = serial.Serial('COM8', 9600)
time.sleep(2)

# Load trained face recognizer model
recognize = c.face.LBPHFaceRecognizer_create()
recognize.read('Trained_model/model.yml')
faceCascade = c.CascadeClassifier('frontalface.xml')

# Font settings
font = c.FONT_HERSHEY_SIMPLEX

# Person ID and names list
names = ['Access', 'Access']

# Open the webcam
cam = c.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

# Minimum size for face detection
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

# Initialize recognizer for voice commands
recognizer = sr.Recognizer()

# Lock to prevent multiple voice threads
voice_command_lock = threading.Lock()

def say(query):
    """Text-to-speech function."""
    if query != "none":
        speaker = pyttsx3.init()
        voices = speaker.getProperty('voices')
        speaker.setProperty('voice', voices[0].id)
        speaker.setProperty('rate', 130)
        speaker.say(query)
        speaker.runAndWait()

def send_command_to_arduino(command):
    """Send command to Arduino."""
    arduino.write(command.encode())

def listen_for_command():
    """Listen for voice commands to control the light."""
    if voice_command_lock.acquire(blocking=False):  # Ensure single thread
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
                print("Listening for command...")
                say("Listening for command.")
                try:
                    audio = recognizer.listen(source, timeout=5)  # Reduce timeout for faster retry
                    command_text = recognizer.recognize_google(audio).lower()
                    print("You said:", command_text)

                    if "turn on light" in command_text:
                        send_command_to_arduino('1')
                        say("Turning on the light.")
                    elif "turn off light" in command_text:
                        send_command_to_arduino('2')
                        say("Turning off the light.")
                    else:
                        say("Command not recognized.")
                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                    say("Sorry, I didn't catch that.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")
                    say("Speech recognition service is unavailable.")
        finally:
            voice_command_lock.release()

# Main loop for face recognition and voice command
while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to capture image from camera.")
        break

    convert_img = c.cvtColor(img, c.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(convert_img, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

    for (x, y, z, h) in faces:
        c.rectangle(img, (x, y), (x + z, y + h), (0, 255, 0), 2)
        id, accuracy = recognize.predict(convert_img[y:y + h, x:x + z])
        accuracy_text = f"{round(100 - accuracy)}%"

        if int(100 - accuracy) > 30:
            id_text = names[id]
            access_granted = True
        else:
            id_text = "Unknown"
            access_granted = False

        c.putText(img, str(id_text), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        c.putText(img, accuracy_text, (x + 5, y + h + 20), font, 1, (255, 255, 255), 1)

        if access_granted:
            if not threading.active_count() > 1:  # Ensure only one voice thread runs
                threading.Thread(target=listen_for_command).start()

    c.imshow('camera', img)

    if c.waitKey(10) & 0xff == 27:  # Press 'ESC' to exit
        break

# Release resources
cam.release()
c.destroyAllWindows()
arduino.close()
