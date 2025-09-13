"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 28/1/2025

Module to extract features from speech
"""

# Importing Dependencies
import numpy as np
import librosa


# Zero Crossing Rate
def zcr(data, frame_length, hop_length):
    
    # Perform ZCR
    zcr = librosa.feature.zero_crossing_rate(
        data,frame_length = frame_length,
        hop_length = hop_length
    )
    
    return np.squeeze(zcr)


# STFT Function
def stft(data, sr, frame_length = 2048, hop_length = 512):
   
    # Perform Short-Time Fourier Transform (STFT)
    stft_result = librosa.stft(
        y = data, 
        n_fft = frame_length, 
        hop_length = hop_length
    )
    
    # Convert the amplitude to decibels
    stft_db = librosa.amplitude_to_db(np.abs(stft_result), ref = np.max)
    
    return stft_db


# RMSE
def rmse(data,frame_length = 2048, hop_length = 512):
    
    # Perform RMSE
    rmse = librosa.feature.rms(
        y = data, 
        frame_length = frame_length, 
        hop_length = hop_length
    )
    
    return np.squeeze(rmse)


# MFCC
def mfcc(data, sr, frame_length = 2048, hop_length = 512, flatten:bool = True):
    
    # Perform MFCC
    mfcc = librosa.feature.mfcc(
        y = data,
        sr = sr
    )
    
    return np.squeeze(mfcc.T)if not flatten else np.ravel(mfcc.T)


# MEL
def mel_spectrogram(data, sr, n_mels = 128, frame_length = 2048, hop_length = 512):
    
    # Perform MEL
    mel_spect = librosa.feature.melspectrogram(
        y = data, 
        sr = sr, 
        n_mels = n_mels, 
        hop_length = hop_length, 
        n_fft = frame_length
    )
    
    return np.squeeze(mel_spect)


# Extracting Features from the Speech
def extract_features(data, sr = 22050, frame_length = 2048, hop_length = 512):

    # Initialize the result array
    result = np.array([])

    # Extract features
    zcr_features = zcr(data, frame_length, hop_length)
    stft_features = stft(data, frame_length, hop_length).flatten()
    rmse_features = rmse(data, frame_length, hop_length)
    mfcc_features = mfcc(data, sr, frame_length, hop_length)
    mel_features = mel_spectrogram(data, sr, frame_length=frame_length, hop_length=hop_length)
    
    # Concatenate features into a single 1D array
    result = np.hstack((
        result,
        zcr_features,
        stft_features,
        rmse_features,
        mfcc_features.flatten() if mfcc_features.ndim > 1 else mfcc_features,
        mel_features.flatten() if mel_features.ndim > 1 else mel_features
    ))
    
    return result
