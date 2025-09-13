"""
NAME: CHEAH WENG HOE
DATE CREATED: 15/2/2025
LAST MODIFIED: 20/2/2025

Module to Fuse SER and TER Model
"""

# Importing Dependencies
import os
import sys
import joblib
import numpy as np

from Models.TER.model import predict_text_emotion_proba
from Models.SER.model import predict_speech_emotion_proba

from engine.command import transcribe_audio, save_temp_audio, record_audio

from tensorflow.keras.models import load_model


# Define Paths
TER_LABEL_PATH = "Models/TER/utils/label_encoder.pkl"
SER_LABEL_PATH = "Models/TER/utils/label_encoder.pkl"


# Load TER Encoder
if os.path.exists(TER_LABEL_PATH):
    text_label_encoder = joblib.load(TER_LABEL_PATH)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)


# Load SER Encoder
if os.path.exists(SER_LABEL_PATH):
    speech_label_encoder = joblib.load(SER_LABEL_PATH)
else:
    print("[ERROR] Saved scaler not found!")
    sys.exit(1)



# Decision Level Fusion
def integrated_emotion_recognition(modality, input_data=None):
   
    if modality.lower() == "text":

        transcript = input_data.strip().lower()
        ter_probs = predict_text_emotion_proba(transcript)  # Get probability output


        # Get highest probability class
        final_emotion_idx = np.argmax(ter_probs)

        # Map index to label using the text label encoder
        final_emotion = text_label_encoder.inverse_transform([final_emotion_idx])[0]

        return final_emotion, transcript
    
    elif modality.lower() == "speech":

        print("Recording audio for emotion recognition...")
        audio, fs = record_audio()

        if audio is None:

            print("[ERROR] No audio recorded!")

            return "neutral", ""
        
        temp_audio_path = save_temp_audio(audio, fs)

        # Step 1: Transcribe the Speech
        transcript = transcribe_audio(temp_audio_path)

        if not transcript:

            print("[ERROR] No transcript generated!")
            os.remove(temp_audio_path)

            return "neutral", ""
        
        # Step 2: Get SER probability prediction
        ser_probs = predict_speech_emotion_proba(temp_audio_path)
        
        # Step 3: Get TER probability prediction
        ter_probs = predict_text_emotion_proba(transcript)
        
        os.remove(temp_audio_path)  # Clean up temporary file


        # Get class indices
        ser_class_idx = np.argmax(ser_probs)
        ter_class_idx = np.argmax(ter_probs)

        # Convert class indices to emotion labels using saved encoders
        ser_emotion = speech_label_encoder.inverse_transform([ser_class_idx])[0]
        ter_emotion = text_label_encoder.inverse_transform([ter_class_idx])[0]
        
        print(f"SER: {ser_emotion}, TER: {ter_emotion}")

        # Fusion Strategy: Weighted Averaging (Default)
        alpha = 0.3  # Weight for speech
        beta = 0.7   # Weight for text
        fused_probs = (alpha * ser_probs) + (beta * ter_probs)

        # Ensure fused_probs sums to 1
        fused_probs /= np.sum(fused_probs)

        # Get the final predicted emotion
        final_emotion_idx = np.argmax(fused_probs)

        if len(text_label_encoder.classes_) == len(speech_label_encoder.classes_):
            final_emotion = text_label_encoder.inverse_transform([final_emotion_idx])[0]
        else:
            # If there's a mismatch in label encoders, create a universal mapping
            emotion_labels = list(set(text_label_encoder.classes_).intersection(set(speech_label_encoder.classes_)))
            final_emotion = emotion_labels[final_emotion_idx] if final_emotion_idx < len(emotion_labels) else "Unknown"

        return final_emotion, transcript
    
    else:
        
        raise ValueError("Modality must be either 'text' or 'speech'.")
    

# # Normal Fusion 
# def integrated_emotion_recognition(modality, input_data=None):
   
#     if modality.lower() == "text":
#         transcript = input_data.strip().lower()
#         emotion = predict_text_emotion(transcript)

#         return emotion, transcript
    
#     elif modality.lower() == "speech":

#         # Step 1: Get Transcript 
#         print("Recording audio for emotion recognition...")
#         audio, fs = record_audio()

#         if audio is None:
#             print("[ERROR] No audio recorded!")

#             return "neutral", transcript
        

#         # Step 2: Save Audio for Emotion Recognition
#         temp_audio_path = save_temp_audio(audio, fs)

#         # Step 3: Transcribe the Speech
#         transcript = transcribe_audio(temp_audio_path)

#         if not transcript:

#             print("[ERROR] No transcript generated!")
#             os.remove(temp_audio_path)  # Clean up temp file

#             return "neutral", ""
        

#         # Step 4: Get SER emotion prediction
#         ser_emotion = predict_speech_emotion(temp_audio_path)
        
        
#         # Step 5: Get TER emotion prediction on the transcript
#         ter_emotion = predict_text_emotion(transcript)
        
#         # Step 6: Clean up temporary file
#         os.remove(temp_audio_path)
#         print(f"SER: {ser_emotion}, TER: {ter_emotion}")
        

#         # Fusion Logic: Prioritize SER, or use agreement
#         final_emotion = ser_emotion if ser_emotion.lower() == ter_emotion.lower() else "mixed"

#         return final_emotion, transcript
    
#     else:
        
#         raise ValueError("Modality must be either 'text' or 'speech'.")