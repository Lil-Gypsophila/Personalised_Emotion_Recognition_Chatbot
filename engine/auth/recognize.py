"""
NAME: CHEAH WENG HOE
DATE CREATED: 29/1/2025
LAST MODIFIED: 29/1/2025

Main Module for Face Authentication
"""


import cv2
import os
import time
import sys
import pyautogui as p

from sys import flags

# Paths
TRAINER_PATH = "engine/auth/trainer/trainer.yml"
SAMPLES_PATH = "engine/auth/samples"


# Global variable to store last recognized user
last_recognized_name = None  


# Face Authentication
def authenticate_face(timeout = 15):

    # Allow updating globally
    global last_recognized_name

    # Load the trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.exists(TRAINER_PATH):
        print("[ERROR] No trained model found. Run `trainer.py` first.")
        sys.exit(1)

    recognizer.read(TRAINER_PATH)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


    # Load user names from directories
    user_names = {0: "Unknown"}
    for folder in os.listdir(SAMPLES_PATH):
        if "_" in folder:
            user_id, user_name = folder.split("_", 1)
            if user_id.isdigit():
                user_names[int(user_id)] = user_name.replace("_", " ")  # Convert back to normal name


    # Initialize webcam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        print("[ERROR] Could not open webcam.")
        sys.exit(1)

    cam.set(3, 640)  # Width
    cam.set(4, 480)  # Height

    minW = int(0.1 * cam.get(3))
    minH = int(0.1 * cam.get(4))

    print("[INFO] Face recognition system initialized. Looking for faces...")

    # To store recognized person's name
    recognized_name = None

    # Track time for timeout  
    start_time = time.time()  


    while True:

        ret, img = cam.read()

        if not ret:
            print("[ERROR] Camera error. Exiting.")
            sys.exit(1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(minW, minH))


        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_crop = gray[y:y+h, x:x+w]

            # Predict the face
            id_, accuracy = recognizer.predict(face_crop)

            # Recognition threshold
            threshold = 70  # Lower means stricter matching
            if accuracy < threshold:
                recognized_name = user_names.get(id_, "Unknown")
                last_recognized_name = recognized_name
                acc_text = f"Match: {round(100 - accuracy)}%"
                text_color = (0, 255, 0)  # Green for recognized faces

                print(f"[SUCCESS] Recognized: {recognized_name} with accuracy: {round(100 - accuracy)}%")


                # Display Name & Accuracy on Screen
                cv2.putText(img, recognized_name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)
                cv2.putText(img, acc_text, (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)

                cam.release()
                cv2.destroyAllWindows()
                print("[DEBUG] Returning: 1,", recognized_name)
                return 1, recognized_name 

            else:

                print(f"[WARNING] Unknown face detected with accuracy: {round(100 - accuracy)}%")
                acc_text = f"Low Confidence"
                text_color = (0, 0, 255)


        cv2.imshow("Face Recognition", img)

        if time.time() - start_time > timeout:
            print("[ERROR] Face authentication timed out. No recognized face found.")
            cam.release()
            cv2.destroyAllWindows()
            return 0, None

        k = cv2.waitKey(10) & 0xFF
        if k == 27:  # Press ESC to exit
            break


    print("[INFO] Shutting down system...")
    cam.release()
    cv2.destroyAllWindows()
    print("[DEBUG] Returning: 0")

    return 0, None  # Return the recognized name
