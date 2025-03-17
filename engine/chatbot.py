"""
NAME: CHEAH WENG HOE
DATE CREATED: 1/2/2025
LAST MODIFIED: 20/2/2025

Module for Chatbot
"""

# Importing Dependencies
import os
from openai import OpenAI

from API.api_keys_handler import load_api_key
from engine.command import text_to_speech


# Retrieve the OpenAI API key
OPENAI_API_KEY = load_api_key("openai")


# Debugging: Check if API Key is loaded
if not OPENAI_API_KEY:
    raise ValueError("[ERROR] OpenAI API Key could not be loaded. Check your JSON file and .env settings.")



# Load OpenAI API Key
client = OpenAI(

    api_key = OPENAI_API_KEY

)

# Initialize conversation history
conversation_history = [
    {
        "role": "system", 
        "content": "You are JARVIS, a virtual assistant. Your task is to provide responses based on the emotions predicted."
    }
]


# Generate Response from OpenAI
def generate_response(prompt):

    global conversation_history

    try:

        # Append the latest user message to conversation history
        conversation_history.append({"role": "user", "content": prompt})

        # limit to last 10 interactions to stay within token limits
        conversation_history = conversation_history[-10:]

        response = client.chat.completions.create(

            # Define OpenAI Model
            model = "gpt-4o",
            messages = conversation_history,
            temperature = 0.7,  # Adjust temperature for creativity vs. determinism
            max_tokens = 150   # Adjust max tokens as needed
        )

        # Extract the chatbot reply from the response object
        chatbot_reply = response.choices[0].message.content.strip()

        # Append the chatbot response to the conversation history
        conversation_history.append({"role": "assistant", "content": chatbot_reply})

        # Convert the generated text to speech
        text_to_speech(chatbot_reply)

        return chatbot_reply
    
    except Exception as e:

        print(f"[ERROR] OpenAI API call failed: {e}")

        return "I'm sorry, I couldn't process that."