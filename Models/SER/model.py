"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 20/2/2024

Module to Handle SER Model
"""

# Importing Dependencies
import os
import sys
import joblib
import librosa

import numpy as np

from Models.SER.data_preprocessing import process_audio
from Models.SER.feature_engineering import extract_features

import tensorflow as tf
from tensorflow.keras.models import load_model


# Define Paths
SPEECH_MODEL = "Models/SER/utils/Best_CNN.h5"
SCALER_PATH = "Models/SER/utils/ser_scaler.pkl"
LABEL_PATH = "Models/TER/utils/label_encoder.pkl"

# Save Extracted Features
FEATURES_DIR_SER = "Models/SER/utils/features/"
os.makedirs(FEATURES_DIR_SER, exist_ok = True)


# Load Model
if os.path.exists(SPEECH_MODEL):
    ser_model = load_model(SPEECH_MODEL)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


# Load Scaler
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


# Load Encoder
if os.path.exists(LABEL_PATH):
    encoder = joblib.load(LABEL_PATH)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


def adjust_feature_length(features, expected_length=2376):

    features = np.array(features)

    current_length = features.shape[0]
    if current_length > expected_length:
        return features[:expected_length]
    
    elif current_length < expected_length:
        pad_length = expected_length - current_length
        return np.pad(features, (0, pad_length), mode='constant')
    
    else:
        return features


# Get the Extracted Features
def get_features(path, duration = 2.5, offset = 0.6, target_sr = 16000, frame_length = 2048, hop_length = 512):
    

    # Data Preprocessing
    data, sr = process_audio(path, target_sr = target_sr, duration = duration)
    
    # Load the audio file with duration and offset (as done in training for aud_1)
    data, sr = librosa.load(path, duration=duration, offset=offset, sr=target_sr)
    
    # Extract features using your feature extraction function
    features = extract_features(data, sr=target_sr, frame_length=frame_length, hop_length=hop_length)

    # Force to extract only 2376 features
    features_adjusted = adjust_feature_length(features, expected_length = 2376)
    
    return features_adjusted





# Functions to predict the emotion from speech (Returning Probabilities)
def predict_speech_emotion_proba(audio_file_path):

    # Extract features using the inference feature extraction function
    features = get_features(audio_file_path, duration=2.5, offset=0.6, target_sr=16000, frame_length=2048, hop_length=512)
    
    # Print feature dimension for debugging (should be 2376)
    print("Extracted features shape:", np.array(features).shape)
    
    # Reshape the feature vector to a 2D array (1 sample, 2376 features)
    features = np.array(features).reshape(1, -1)
    
    # Scale the features using the saved scaler
    features_scaled = scaler.transform(features)
    
    # Reshape to add channel dimension if needed by the CNN model (e.g., (1, 2376, 1))
    features_scaled = features_scaled.reshape(features_scaled.shape[0], features_scaled.shape[1], 1)
    
    # Get Probability predictions
    pred_probs = ser_model.predict(features_scaled).flatten()
    
    return pred_probs
