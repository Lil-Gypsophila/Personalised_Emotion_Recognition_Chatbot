"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 28/1/2025

Module to Handle Eel
"""

# Importing Dependencies
import sys

# Import Functions from other modules
from engine.features import *
from engine.command import *
from engine.auth import recognize

# Initialise Eel
def start_system():

    try:
        print("[INFO] Starting system...")
        eel.init("templates")
        
        # Play startup sound
        play_start_sound()

        @eel.expose
        def init():

            eel.hideLoader()
            
            # Face Authentication
            text_to_speech("Ready for Face Authentication")
            authentication, user_name = recognize.authenticate_face()

            print(f"[DEBUG] Authentication Result: {authentication}")

            if authentication == 1:

                print(f"[SUCCESS] Welcome, {user_name}!")
                eel.hideFaceAuth()
                text_to_speech(f"Authenticated. Welcome, {user_name}")
                eel.hideFaceAuthSuccess()
                eel.hideStart()

                # Play startup sound
                play_start_sound()

            else:

                print("[ERROR] Face authentication failed.")
                text_to_speech("Face Authentication Failed")
                stop_eel()

        # Launch web application in Edge
        os.system('start msedge.exe --app="http://localhost:8000/index.html"')

        # Start the Eel server
        eel.start('index.html', mode=None, host='localhost', block=True)

    except Exception as e:

        print(f"[ERROR] Eel startup failed: {e}")


# To run hotword
def listen_hot_word():
        
    try:

        print("[INFO] Hotword detection started.")
        detect_start_word()

    except Exception as e:

        print(f"[ERROR] Hotword detection failed: {e}")


# Stop eel
# https://stackoverflow.com/questions/68029882/how-to-close-eel-or-start-code-with-a-separate-process#:~:text=The%20simplest%20way%20is%20to%20hook%20the%20close_callback%3A,you%20can%20just%20continue%20your%20work%20in%20python.
def stop_eel():

    try:

        # Call JavaScript function to close the window
        eel.close_window()  # ✅ Closes the browser window via JavaScript
        time.sleep(2)  # Allow time for the window to close

    except Exception as e:

        print(f"[WARNING] Could not close Eel browser: {e}")

    # Exit Python
    sys.exit(1)