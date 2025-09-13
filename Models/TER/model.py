"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 20/2/2024

Module to Handle TER Model
"""

# Importing Dependencies
import os
import sys
import joblib
import numpy as np

from Models.TER.data_preprocessing import preprocess_text

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences



# Define Paths
TEXT_MODEL = "Models/TER/utils/Best_Bi_LSTM.h5"
TOKEN_PATH = "Models/TER/utils/tokenizer.pkl"
LABEL_PATH = "Models/TER/utils/label_encoder.pkl"


# Load Model
if os.path.exists(TEXT_MODEL):
    model = load_model(TEXT_MODEL)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


# Load Tokenizer
if os.path.exists(TOKEN_PATH):
    tokenizer = joblib.load(TOKEN_PATH)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


# Load Label Encoder
if os.path.exists(LABEL_PATH):
    le = joblib.load(LABEL_PATH)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


# Functions to predict the emotion from text (Returning Probabilities)
def predict_text_emotion_proba(text):
    processed_text = preprocess_text(text)
    
    # Tokenize and pad
    sequence = tokenizer.texts_to_sequences([processed_text])
    maxlen = 229
    padding_sequence = pad_sequences(sequence, maxlen=maxlen, truncating='pre')

    # Get probability predictions
    pred_probs = model.predict(padding_sequence)

    # Add a dummpy probability for the missing class
    pred_probs = np.append(pred_probs, 0.0)

    return pred_probs  # Ensure 1D output


# Functions to predict the emotion from text
def predict_text_emotion(text):

    # Text Processing
    processed_text = preprocess_text(text)

    # Tokenize and padding
    sequence = tokenizer.texts_to_sequences([processed_text])
    maxlen = 229
    padding_sequence = pad_sequences(sequence, maxlen = maxlen, truncating = 'pre')

    # Prediction
    prediction = model.predict(padding_sequence)
    emotion = le.inverse_transform([prediction.argmax()])[0]

    return emotion