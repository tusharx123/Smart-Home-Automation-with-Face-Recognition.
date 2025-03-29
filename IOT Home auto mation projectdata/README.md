# Face Recognition Project Documentation

## Introduction

This project is designed to capture, train, and recognize faces in real-time using a webcam. The system includes three main components: capturing face samples, training a face recognition model, and recognizing faces using the trained model.

## Table of Contents

- **Setup and Installation**
- **Capturing Face Samples**
- **Training the Model**
- **Recognizing Faces**
- **Usage**
- **Dependencies**
- **Acknowledgments**

## Setup and Installation

### Prerequisites

Clone Repository

```bash
Git clone https://github.com/147Ayush/Face-Detection-Model.git
```

Ensure you have Python and the necessary libraries installed. You can install the required libraries using pip:
```bash
pip install -r requirements.txt
```

File Structure
```
face_recognition_project/
│
├── sample/                # Directory to store face samples
├── Trained_model/         # Directory to store the trained model
│
├── Sample_Photos.py       # Script for capturing face samples
├── Model_trainer.py       # Script for training the face recognition model
├── Face_recognization.py  # Script for recognizing faces using the trained model
├── frontalface.xml        # Haar cascade file for face detection
├── README.md              # Project documentation
├── requirements.txt       # Dependencies
```
## Capturing Face Samples

The first step is to capture face samples for each user. The capture_samples.py script captures 100 face samples through the webcam and saves them in the sample directory. Each face sample is saved with a unique identifier for each user.

### Process

- Run the script to start the webcam and begin capturing face samples.
- Position the user's face in front of the webcam.
- The script will automatically capture 100 samples and save them in the specified directory.

## Training the Model 

Once you have captured the face samples, the next step is to train the face recognition model using these samples. The train_model.py script processes the samples and trains a model to recognize faces.

### Process

- The script reads the images from the sample directory.
- It converts the images to grayscale and detects faces.
- The detected faces are used to train the LBPH (Local Binary Patterns Histograms) face recognizer.
- The trained model is saved in the Trained_model directory.

## Recognizing Faces

he final step is to recognize faces in real-time using the trained model. The recognize_face.py script uses the webcam to detect and recognize faces.

### Process

- Run the script to start the webcam and begin real-time face recognition.
- The script converts each video frame to grayscale and detects faces.
- For each detected face, the script predicts the identity using the trained model.
- If the predicted accuracy is above a certain threshold, the face is recognized and labeled; otherwise, it is labeled as "Unknown."

## Usage

### Steps to Use the Project

1. Capture Face Samples:

   - Run Sample_photos.py.
   - Follow the on-screen instructions to capture face samples.

2. Train the Model:

   - Run model_tranier.py.
   - Wait for the training process to complete.
      Recognize Faces:

3. Run Face_recognization.py.

   - The script will start the webcam and recognize faces in real-time.
 
## Acknowledgments
This project utilizes the OpenCV library for computer vision tasks and the PIL library for image processing. The face recognition model is based on the LBPH algorithm, which is effective for real-time face recognition applications.