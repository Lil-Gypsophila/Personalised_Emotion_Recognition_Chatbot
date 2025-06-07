"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 20/2/2025

Module to Run the system
"""

# Importing Dependencies
import os
import sys
import multiprocessing

# Import All Functions from eel handler
from engine.eel_handler import *
from engine.chatbot import generate_response

# Importing Models
from Models.fusion import integrated_emotion_recognition


# Main Execution
if __name__ == '__main__':

    try:

        # Create multiprocessing processes
        p1 = multiprocessing.Process(target = start_system)  # Process for Eel
        p2 = multiprocessing.Process(target = listen_hot_word)  # Process for hotword detection

        # Start both processes
        p1.start()
        p2.start()

        # Ensure p1 runs first and completes before checking p2
        p1.join()

        # Ensure p2 stops after p1
        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("[INFO] System stopped.")

    except KeyboardInterrupt:

        print("\n[INFO] System interrupted by user. Shutting down...")

        if p1.is_alive():
            p1.terminate()

        if p2.is_alive():
            p2.terminate()

    except Exception as e:
        
        print(f"[ERROR] Unexpected system failure: {e}")


    # # Debugging for SER
    # audio_test_path = "Models/SER/utils/1001_IEO_SAD_MD.wav" 

    # if not os.path.exists(audio_test_path):
    #     print(f"[ERROR] Audio file not found: {audio_test_path}")
    #     sys.exit(1)
    
    # predicted_emotion = predict_speech_emotion(audio_test_path)
    
    # print("Predicted Speech Emotion:", predicted_emotion)


    # # Debugging for TER
    # sample_text = "I am feeling very joyful today!"
    # predicted_emotion = predict_text_emotion(sample_text)
    # print("Predicted Emotion:", predicted_emotion)


    # # Debugging OpenAI Chatbot
    # prompt = "Predicted Emotion:Sad message:I am sad. What can I do?"
    # reply = generate_response(prompt)
    # print("Chatbot reply:", reply)