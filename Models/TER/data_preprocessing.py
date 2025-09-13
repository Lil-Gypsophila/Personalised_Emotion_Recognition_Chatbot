"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 24/12/2024

Module to pre-process the text
"""

import re
import nltk
import contractions
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Initialising stopwords
stop_words = set(stopwords.words('english') + list(string.punctuation))

# Initialise Lemma
lemmatizer = WordNetLemmatizer()


# Function to change all text to lowercase
def lower_case(text):
    
    text = text.split()

    text = [y.lower() for y in text]
    
    return " " .join(text)


# Functions to fix text contractions
def fix_contractions(text):

    text = text.split()
    
    text = [contractions.fix(word) for word in text]
    
    return " ".join(text)


# Functions to remove noise from the text data
def remove_noise(text):

    # Ensure the text is a string
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    return text


# Function to remove stopwords
def remove_stop_words(text):
    
    Text = [i for i in str(text).split() if i not in stop_words]
    
    return " ".join(Text)


# Function for lemmatization
def lemmatization(text):

    text = text.split()

    text = [lemmatizer.lemmatize(y) for y in text]
    
    return " " .join(text)


# Pre-process the text
def preprocess_text(text):

    text = lower_case(text)
    text = fix_contractions(text)
    text = remove_noise(text)
    text = remove_stop_words(text)
    text = lemmatization(text)
    
    return text