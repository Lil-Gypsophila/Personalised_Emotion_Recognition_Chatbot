"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 28/1/2025

Module to pre-process the speech
"""

# Importing Dependencies
import numpy as np
import librosa


# Resampling
def resample_audio(file_path, target_sr = 16000):
    
    data, sr = librosa.load(file_path, sr = None)
    
    if sr != target_sr:
        data = librosa.resample(data, orig_sr = sr, target_sr = target_sr)
        
    return data, target_sr


# Trimming
def trim_audio(data, top_db = 20):
    
    trimmed_data, _ = librosa.effects.trim(data, top_db = top_db)
    
    return trimmed_data


# Normalisation
def normalize_audio(data):
    
    max_amplitude = np.max(np.abs(data))
    
    if max_amplitude > 0:
        data = data / max_amplitude
        
    return data


# Fix audio length
def fix_audio_length(data, target_length, sr):
    
    target_samples = int(target_length * sr)
    
    if len(data) > target_samples:  # Truncate
        data = data[:target_samples]
        
    elif len(data) < target_samples:  # Pad
        
        pad_length = target_samples - len(data)
        data = np.pad(data, (0, pad_length), mode = 'constant')
        
    return data


# Function to process the audio: resample and normalize
def process_audio(file_path, target_sr = 16000, duration = 2.5):
    
    # Load and resample audio
    data, sr = librosa.load(file_path, sr = target_sr)

    # Trim leading/trailing silence
    data = trim_audio(data)

    # Normalize amplitude
    data = normalize_audio(data)

    # Fix the audio length to ensure consistent feature dimensions
    data = fix_audio_length(data, target_length=duration, sr=sr)

    return data, sr