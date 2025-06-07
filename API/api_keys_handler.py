"""
NAME: CHEAH WENG HOE
DATE CREATED: 17/2/2025
LAST MODIFIED: 17/2/2025

Module to handle API keys
"""

import os
import json
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Function to load API keys from JSON file
def load_api_key(service_name):

    api_key_path = os.getenv("API_KEY_PATH")

    if not api_key_path:
        raise ValueError("API_KEY_PATH is not set in the environment variables.")
    
    try:

        with open(api_key_path, "r") as file:

            data = json.load(file)

        # Check if the requested service exists in the JSON file
        if service_name in data["api_keys"]:

            return data["api_keys"][service_name]
        
        else:

            print(f"[WARNING] API key for '{service_name}' not found.")

            return None
    
    except Exception as e:

        print(f"[ERROR] Failed to load API key: {e}")

        return None


# # Debugging: Print the loaded API key
# openai_key = load_api_key("openai")

# if openai_key:
#     print(f"OpenAI API Key Loaded: {openai_key[:5]}****")
# else:
#     print("[ERROR] OpenAI API Key could not be loaded!")