import cv2 as c
from AppOpener import open, close

# Creating a video capture object to capture video through the webcam
camera = c.VideoCapture(0, c.CAP_DSHOW)

# Setting frame width and height
camera.set(3, 640)
camera.set(4, 480)

# Loading the CascadeClassifier for face detection
detect = c.CascadeClassifier('frontalface.xml')

# Taking unique ID for each user
f_id = int(input("Enter numerical ID: "))

print("Take your face in front of the webcam for samples")

count = 0
while True:
    ret, image = camera.read()  # Reading frames
    if not ret:  # Check if frame is captured successfully
        print("Failed to capture an image from the webcam. Exiting...")
        break

    # Converting the captured image to grayscale for effective face detection
    convert_img = c.cvtColor(image, c.COLOR_BGR2GRAY)
    faces = detect.detectMultiScale(convert_img, 1.3, 5)

    for (x, y, z, h) in faces:
        c.rectangle(image, (x, y), (x + z, y + h), (255, 0, 0), 2)  # Draw rectangle
        count += 1

        # Save the captured image as a sample in the sample folder
        c.imwrite("sample/face." + str(f_id) + '.' + str(count) + ".jpg", convert_img[y:y+h, x:x+z])
        c.imshow('image', image)

    # Wait for a key press for 100 milliseconds
    a = c.waitKey(100) & 0xff
    if a == 27:  # Press ESC to stop
        break
    elif count >= 100:  # Take 100 samples
        break

print("Samples are taken. Now closing the program.")
camera.release()
c.destroyAllWindows()
