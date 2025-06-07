"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 19/2/2025

Module to Handle Features of the System
"""

import eel
import os
import threading
import logging
import webbrowser
import struct
import pvporcupine
import pyaudio
import pywhatkit as kit

# Play start sound
from playsound import playsound

# Import Functions from other folders
from engine.command import *
from engine.helper import *


# Initialise Assistant Name
ASSISTANT_NAME = "Jarvis"

# Function Start Sound
@eel.expose
def play_start_sound():

    # Define the directory
    snd_dir = "templates\\static\\assets\\audio\\start_sound.mp3" 

    # Play the sound
    playsound(snd_dir)


# Function to perform tasks
def func_perform_tasks(query):
    
    # Clean and process the query
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()

    # Normalize app name to avoid mismatches
    # print(f"Processed Query Before Search: '{query}'")
    app_name = re.sub(r'[^\w\s]', '', query.strip().lower())
    # print(f"Searching for: '{app_name}' in the database")

    if app_name:

        try:

            # Check for system paths
            results = fetch_from_db('SELECT path FROM sys_path WHERE name = ?', (app_name,))
            # print(f"Database Query Results for sys_path: {results}")  # Debugging line

            if results:

                # Open application
                path = results[0][0] # Access the first column of the first result (path)
                text_to_speech(f"Opening {query}")
                os.startfile(path) # Opens the application

                return
                

            # Check for web paths
            results = fetch_from_db('SELECT url FROM web_path WHERE name = ?', (app_name,))
            # print(f"Database Query Results for web_path: {results}")  # Debugging line
            
            if results:

                # Open web URL
                url = results[0][0]
                # print(f"Opening URL: {url}")  # Debugging statement
                text_to_speech(f"Opening {query}")
                webbrowser.open(url)
                
                return

            # If no matches were found, attempt to directly execute the command
            text_to_speech(f"Opening {query}")

            try:

                # Attempt to open using system commands
                os.startfile(query)  

            except Exception as ex:

                # Open as a web search
                webbrowser.open(f"https://www.google.com/search?q={query}")
                logging.error(f"Error executing {query} as a command: {ex}")

        except Exception as e:

            # Handle unexpected errors
            text_to_speech("Oops, something went wrong.")
            logging.error(f"Error processing '{query}': {e}")


# Function to perform tasks on YT
def play_youtube(query):

    search_term = extract_yt_term(query)

    if not search_term:  # Double-check if search_term is None
        search_term = "popular videos"  # Set default value

    text_to_speech("Playing "+search_term+" on YouTube")

    def play():
        kit.playonyt(search_term)

    # Run YouTube in a background thread to avoid blocking the main function
    thread = threading.Thread(target=play, daemon=True)
    thread.start()

    print(f"[INFO] Playing '{search_term}' on YouTube.")


# Function to Detect Start Word
def detect_start_word():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key alt+j
                import pyautogui as autogui
                autogui.keyDown("alt")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("alt")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()