"""
NAME: CHEAH WENG HOE
DATE CREATED: 29/1/2025
LAST MODIFIED: 29/1/2025

Module to take samples for Face Authentication
"""

import cv2
import os


# Function to generate a unique ID based on existing folders
def generate_face_id():
    
    existing_ids = [int(folder.split("_")[0]) for folder in os.listdir(BASE_DIR) if folder.split("_")[0].isdigit()]

    return max(existing_ids, default = 0) + 1  # Assign the next available ID


# Define Path to save the face samples
BASE_DIR = "engine/auth/samples"
os.makedirs(BASE_DIR, exist_ok = True)


# Get user details
user_name = input("Enter your name: ").strip().replace(" ", "_")  # Replace spaces with underscores

if not user_name:
    print("[ERROR] Name cannot be empty!")
    exit()

# Auto Generate ID
face_id = generate_face_id()

# Define path to store user samples
user_folder = os.path.join(BASE_DIR, f"{face_id}_{user_name}")
os.makedirs(user_folder, exist_ok = True)


# Capturing Sample Message
print(f"[INFO] Capturing samples for {user_name} (ID: {face_id})... Look at the camera.")

# Initialize webcam
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
cam.set(3, 640) # set video FrameWidth
cam.set(4, 480) # set video FrameHeight


# Load Haar Cascade for face detection
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Calculate number of samples
count = 0

while True:

    ret, img = cam.read() 

    if not ret:
        print("[ERROR] Camera error. Exiting.")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = detector.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5, minSize = (30, 30))

    for (x, y, w, h) in faces:

        # Draw a rectangle to capture only the face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        count += 1

        # Save face sample in user's folder
        img_path = os.path.join(user_folder, f"face.{face_id}.{count}.jpg")
        cv2.imwrite(img_path, gray[y : y + h, x : x + w])


        # Display an image in a window
        cv2.imshow('image', img) 

    k = cv2.waitKey(100) & 0xff # Waits for a pressed key
    if k == 27 or count >= 100: # Press 'ESC' to stop
        break

print(f"[INFO] Samples for {user_name} (ID: {face_id}) collected successfully.")
cam.release()
cv2.destroyAllWindows()