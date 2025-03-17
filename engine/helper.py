"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 28/1/2025

Helper Functions
"""

import os
import re
import time
import sqlite3
import logging


# Helper Function to Extract YT terms
def extract_yt_term(command):

    # Cleans punctuation and spaces before extracting
    command = command.strip().lower()  # Remove extra spaces & lowercase
    command = re.sub(r'[^\w\s]', '', command)  # Remove punctuation

    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube$'

    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)

    # If a match is found, return the extracted song name; otherwise, return None
    if match:
        return match.group(1)
    else:
        print("[ERROR] No valid search term found in query.")
        return "popular videos"  # Default fallback term


# Helper Function to execute SQL
def fetch_from_db(query, params = ()):

    try:
        conn = sqlite3.connect(r"database\debs.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    except Exception as e:

        logging.error(f"Database Error: {e}")
        return []


# Function to
def remove_words(input_string, words_to_remove):

    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string



# key events like receive call, stop call, go back
def keyEvent(key_code):
    command =  f'adb shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

# Tap event used to tap anywhere on screen
def tapEvents(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

# Input Event is used to insert text in mobile
def adbInput(message):
    command =  f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

# To replace space in string with %s for complete message send
def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')
