"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 20/2/2025

Module to Handle Commands
"""

import os
import tempfile
import queue
import time
import logging

import eel
import pyttsx3
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np

from openai import OpenAI
from API.api_keys_handler import load_api_key


# Load Whisper model
# https://www.gyan.dev/ffmpeg/builds/
# whisper_model = whisper.load_model("medium")  # use "small", "medium", or "large" for better accuracy


# Load OpenAI API Key
openai_api_key = load_api_key("openai")

# Initialize OpenAI Client
client = OpenAI(api_key=openai_api_key)


# Function to convert text to speech
def text_to_speech(text):

    try:
        # Ensure text is in string format
        text = str(text)
        
        # Display the text
        eel.DisplayMessage(text)
        eel.receiverText(text)  # Save in chat history

        # Generate speech using OpenAI's TTS-1 model
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "nova",  # Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
            input = text
        )

        # Save the audio to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file.write(response.content)
        temp_file.close()

        # Read and play the audio
        data, sample_rate = sf.read(temp_file.name)
        sd.play(data, sample_rate)
        sd.wait()

        # Remove after read
        os.remove(temp_file)

    except Exception as e:
        print(f"[ERROR] TTS-1 failed: {e}")

    # # Configuring
    # text = str(text)
    # engine = pyttsx3.init('sapi5')
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id)
    # engine.setProperty('rate', 170)

    # # Display the text
    # eel.DisplayMessage(text)

    # # Converting text to speech
    # engine.say(text)
    # eel.receiverText(text) # Save in chat history
    # engine.runAndWait()


# Recording Audio
def record_audio(fs=16000, silence_duration=2, silence_threshold=0.02, chunk_duration=0.5):

    print("🎤 Recording... Speak now.")

    q = queue.Queue()
    silence_start = None  # Ensure it's initialized
    speech_detected = False  # Track if speech has started

    def callback(indata, frames, time, status):
        if status:
            print(f"Status: {status}")
        q.put(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        audio_chunks = []

        while True:  # Continuous recording until silence is detected
            if q.empty():
                time.sleep(0.01)
                continue

            chunk = q.get()
            rms = np.sqrt(np.mean(chunk ** 2))  # Calculate RMS for silence detection

            if rms > silence_threshold:
                if not speech_detected:
                    print("🎙️ Speech detected, recording...")
                speech_detected = True
                silence_start = None  # Reset silence timer when speech is detected
                audio_chunks.append(chunk)

            elif speech_detected:  # ✅ Only check silence after speech was detected
                if silence_start is None:  # CORRECTLY Initialize silence_start
                    silence_start = time.time()
                elif (time.time() - silence_start) > silence_duration:
                    print("Silence detected. Stopping recording...")
                    break  # Stop recording when silence is detected for `silence_duration`

    if not audio_chunks:
        print("[❌ ERROR] No audio recorded!")
        return None, fs  # Return None if no speech was detected

    audio = np.concatenate(audio_chunks, axis=0)
    audio = np.squeeze(audio)

    print("Recording finished.")
    
    return audio, fs

# Function to Recognize Speech
@eel.expose
def speech_recognition():

    # Display Status
    print("Listening...")
    eel.DisplayMessage("Listening...")

    # Record the user's speech
    audio, sample_rate = record_audio()

    if audio is None:
        print("[ERROR] No audio recorded!")

        return None
    
    # Save as temporary file
    audio_file_path = save_temp_audio(audio, sample_rate)


    # Send to OpenAI Whisper API
    print("Recognizing speech...")
    eel.DisplayMessage("Recognizing...")

    try:
        with open(audio_file_path, "rb") as audio_file:

            result = client.audio.transcriptions.create(
                model = "whisper-1",
                file = audio_file,
                language = "en"
            )

        transcript = result.text.strip().lower()
        
    except Exception as e:

        print(f"[ERROR] Whisper API failed: {e}")

        return None

    # Display recognized text
    print(f"Recognized Text: {transcript}")
    eel.ShowHood()

    return transcript


# # Debugging
# text = speech_recognition()
# text_to_speech(text)


# Function to handle assistance tasks
@eel.expose
def perform_tasks(message = 1):

    transcript = ""

    try:

        # Use speech recognition if message is not provided
        if message == 1:

            # For speech input, record and process
            from Models.fusion import integrated_emotion_recognition

            emotion, transcript = integrated_emotion_recognition(modality = "speech")
    
        else:
            
            # For text input, use the provided text
            from Models.fusion import integrated_emotion_recognition

            emotion, transcript = integrated_emotion_recognition(modality = "text", input_data=message)


        # Ensure transcript is a string before using `.strip()`
        transcript = str(transcript).strip().lower()
        eel.senderText(transcript)

        if "open" in transcript or "on youtube" in transcript:

            if "open" in transcript:

                from engine.features import func_perform_tasks
                func_perform_tasks(transcript)

                eel.ShowHood()

                return  # Exit early

            elif "on youtube" in transcript:

                from engine.features import play_youtube
                play_youtube(transcript)

                eel.ShowHood()
                
                return  # Exit early
        
        # Debugging
        print(f"[INFO] Recognized Query: '{transcript}' | Emotion: {emotion}")


        # Send Query & Emotion to OpenAI
        from engine.chatbot import generate_response

        # Define the Prompt with predicted emotions
        prompt = f"The user appears to be {emotion} and said: '{transcript}'. Respond in a way that is appropriate for that emotion."
        
        # Generate Response
        chatbot_reply = generate_response(prompt)

        # Debugging
        print("Chatbot reply:", chatbot_reply)
    
    except Exception as ex:

        logging.error(f"Error processing '{transcript}': {ex}")


    # Return Back to the Hood
    eel.ShowHood()


# Saving the audio for prediction
def save_temp_audio(recording, fs):

    # Save the audio file as temp file
    temp_file = tempfile.NamedTemporaryFile(suffix = ".wav", delete = False)
    sf.write(temp_file.name, recording, fs)

    return temp_file.name


# Transcribe speech from an audio file using OpenAI Whisper API
def transcribe_audio(audio_file_path):

    if not os.path.exists(audio_file_path):
        print(f"[ERROR] Audio file {audio_file_path} not found!")
        return None

    try:
        with open(audio_file_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model = "whisper-1",
                file = audio_file,
                language = "en"
            )
        return result.text.strip().lower()

    except Exception as e:

        print(f"[ERROR] Whisper failed: {e}")

        return None