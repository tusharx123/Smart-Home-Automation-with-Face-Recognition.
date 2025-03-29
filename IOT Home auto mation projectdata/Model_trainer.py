import cv2 as c
from PIL import Image
import numpy as np
import os

path = 'sample'
recognize = c.face.LBPHFaceRecognizer.create()
detect = c.CascadeClassifier("frontalface.xml")

def img_labels(path):
    imgpaths = [os.path.join(path,f) for f in os.listdir(path)]
    f_samples = [] #empty list to store image as binary code
    ids = []

    for imgpath in imgpaths:#loop for take each picture and convert it into binary code
        gray_image = Image.open(imgpath).convert('L')
        image_array = np.array(gray_image,'uint8')#change it into integer

        id = int(os.path.split(imgpath)[-1].split(".")[1])
        faces = detect.detectMultiScale(image_array)

        for (x,y,z,h) in faces:
            f_samples.append(image_array[y:y+h,x:x+z])#rectangle
            ids.append(id)#adding in to list

    return f_samples,ids
print("Training model, so It will take time, that's why please wait")

faces, ids = img_labels(path)
recognize.train(faces, np.array(ids))

recognize.write('Trained_model/model.yml')
print("model trained")
