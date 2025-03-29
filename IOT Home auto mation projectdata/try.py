import cv2 as c
import speech_recognition as sr
import threading
import pyttsx3

# Load trained face recognizer model
recognize = c.face.LBPHFaceRecognizer.create()
recognize.read('Trained_model/model.yml')
faceCascade = c.CascadeClassifier('frontalface.xml')

# Font settings
font = c.FONT_HERSHEY_SIMPLEX

# Person ID and names list
names = ['Acess', 'Acess']  # Add more names as needed

# Open the webcam
cam = c.VideoCapture(0, c.CAP_DSHOW)
cam.set(3, 640)  # Frame width
cam.set(4, 480)  # Frame height

# Minimum size for face detection
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

# Lock to prevent multiple voice threads
voice_command_lock = threading.Lock()

def say(query):
    if query == "none":
        pass
    else:
        speaker = pyttsx3.init()
        voices = speaker.getProperty('voices')
        speaker.setProperty('voice', voices[0].id)
        speaker.setProperty('rate', 130)
        speaker.say(query)
        speaker.runAndWait()
        speaker.stop()

# New voice recognition method without loop
def recog():
    """
    Listens for a single speech command and returns the recognized text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        r.pause_threshold = 0.7  # Set pause threshold for better recognition

        print("Listening for a command...")
        say("Please give a command.")

        try:
            audio = r.listen(source, timeout=5)  # Timeout after 5 seconds if no command is given
            command_text = r.recognize_google(audio, language="en-IN")  # Recognize speech
            print(f"Recognized command: {command_text}")
            return command_text

        except sr.UnknownValueError:
            say("I could not understand the command.")
            return "Unknown Command"
        except sr.RequestError:
            say("Sorry, there was an issue with the speech recognition service.")
            return "Recognition Service Error"
        except Exception as e:
            say("Sorry, something went wrong.")
            return "Error"

# Initialize threading lock for safe access to shared variables
lock = threading.Lock()

# Variable to store and display the recognized command on screen
recognized_command = ""

while True:
    ret, img = cam.read()
    convert_img = c.cvtColor(img, c.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(convert_img, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

    for (x, y, z, h) in faces:
        c.rectangle(img, (x, y), (x + z, y + h), (0, 255, 0), 2)
        id, accuracy = recognize.predict(convert_img[y:y + h, x:x + z])  # Predict face ID
        accuracy_text = f"{round(100 - accuracy)}%"

        if int(100 - accuracy) > 30:
            id_text = names[id]
            access_granted = True
        else:
            id_text = "Unknown"
            access_granted = False

        c.putText(img, str(id_text), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        c.putText(img, accuracy_text, (x + 5, y + h + 20), font, 1, (255, 255, 255), 1)

        # If access is granted, start the voice recognition thread if it's not already running
        if access_granted and not voice_command_lock.locked():
            def process_command():
                global recognized_command
                recognized_command = recog()  # Call recog() and store result
            threading.Thread(target=process_command).start()

    # Display the recognized command on the video feed
    c.putText(img, "Command: " + recognized_command, (10, 50), font, 1, (0, 255, 0), 2)

    c.imshow('camera', img)

    if c.waitKey(10) & 0xff == 27:
        break

cam.release()
c.destroyAllWindows()
