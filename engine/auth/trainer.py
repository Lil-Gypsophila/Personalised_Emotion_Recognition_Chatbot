"""
NAME: CHEAH WENG HOE
DATE CREATED: 29/1/2025
LAST MODIFIED: 29/1/2025

Module to train samples for Face Authentication
"""

import cv2
import numpy as np
from PIL import Image
import os


# Paths
BASE_DIR = 'engine/auth/samples'
TRAINER_DIR = 'engine/auth/trainer'
os.makedirs(TRAINER_DIR, exist_ok = True)

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def get_images_and_labels():
    face_samples = []
    ids = []

    for user_folder in os.listdir(BASE_DIR):  # Scan all user directories
        folder_path = os.path.join(BASE_DIR, user_folder)

        if os.path.isdir(folder_path):  # Only process directories
            user_id = int(user_folder.split("_")[0])  # Extract user ID from folder name

            for image_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_name)
                
                gray_img = Image.open(image_path).convert('L')
                img_arr = np.array(gray_img, 'uint8')

                faces = detector.detectMultiScale(img_arr, scaleFactor=1.2, minNeighbors=5)
                
                for (x, y, w, h) in faces:
                    face_samples.append(img_arr[y:y+h, x:x+w])
                    ids.append(user_id)

    return face_samples, ids

print("[INFO] Recognising Face. Please wait...")


# Get the sample image and train the model
faces, ids = get_images_and_labels()
recognizer.train(faces, np.array(ids))


# Save the trained model
recognizer.save(os.path.join(TRAINER_DIR, 'trainer.yml'))
print("[INFO] Model trained successfully.")