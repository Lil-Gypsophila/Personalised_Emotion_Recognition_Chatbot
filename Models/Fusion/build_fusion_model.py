"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 28/1/2025

Module to Run the system
"""



import os
import sys
import random
import numpy as np
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
import tensorflow.keras.layers as L
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint


# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Models.TER.model import extract_text_features
from Models.SER.model import extract_speech_features



# # Loading TER Dataset
def load_ter_dataset(text_file_path):

    texts, labels = [], []
    
    with open(text_file_path, "r", encoding="utf-8") as file:

        for line in file:
            parts = line.strip().split(";")

            if len(parts) == 2:
                labels.append(parts[1].strip())  # Emotion label
                texts.append(parts[0].strip())  # Text sentence
                
    return texts, labels


# Loading SER Dataset
def load_ser_dataset(csv_file_path):
    df = pd.read_csv(csv_file_path)

    audio_paths = df['path'].tolist()
    labels = df['emotion'].tolist()

    return audio_paths, labels


# Encode emotion labels 
def encode_labels(labels, save_path = "Models/Fusion/utils/hybrid_encoder.pkl"):
    label_encoder = LabelEncoder()
    integer_labels = label_encoder.fit_transform(labels)
    encode_labels = to_categorical(integer_labels)

    # Save the encoder
    joblib.dump(label_encoder, save_path)

    return encode_labels, label_encoder


# Loading Dataset
data_dir = "Models/Dataset" 

text_train_samples, text_train_labels = load_ter_dataset(os.path.join(data_dir, "Text/train.txt"))
audio_train_samples, audio_train_labels = load_ser_dataset(os.path.join(data_dir, "Speech/speech_data.csv"))

# Text Data
text_data = list(zip(text_train_samples, text_train_labels))    # Zip text samples and labels to keep them aligned during shuffling
random.shuffle(text_data)
text_train_samples, text_train_labels = zip(*text_data)         # Unzip after shuffling
text_train_samples = text_train_samples[:10000]

text_train_samples = list(text_train_samples[:10000])       # Convert to lists and limit to 10,000 samples
text_train_labels = list(text_train_labels[:10000])

# Speech Data
speech_data = list(zip(audio_train_samples, audio_train_labels))
random.shuffle(speech_data)
audio_train_samples, audio_train_labels = zip(*speech_data)

audio_train_samples = list(audio_train_samples[:10000])
audio_train_labels = list(audio_train_labels[:10000])


# Encode Labels
text_train_labels_encoded, label_encoder = encode_labels(text_train_labels)
audio_train_labels_encoded, _ = encode_labels(audio_train_labels)

# print("Label Mapping:", label_encoder.classes_)

# # Check one-hot encoded labels
# print("First Text Label (One-Hot):", text_train_labels_encoded[0])
# print("First Speech Label (One-Hot):", audio_train_labels_encoded[0])

# Feature Extraction
print("Extracting Features for Training...")


# Extract Text Features
text_train_features = []
for idx, text in enumerate(text_train_samples):

    ter_features = extract_text_features(text, text_id = f"text_{idx}")

    if ter_features is not None:
        text_train_features.append(ter_features)

text_train_features = np.array(text_train_features)


# Extract Speech Features
speech_train_features = []
for idx, audio_path in enumerate(audio_train_samples):
    
    ser_features = extract_speech_features(audio_path, audio_id = f"audio_{idx}")

    if ser_features is not None:
        speech_train_features.append(ser_features)

speech_train_features = np.array(speech_train_features)

print(f"Extracted Text Feature Shape: {text_train_features.shape}")  # Expected: (N, 128)
print(f"Extracted Speech Feature Shape: {speech_train_features.shape}")  # Expected: (10, 256)



print("Feature Extraction Complete! Starting Training...")



# Define Fusion Model
def build_fusion_model(text_feature_dim, speech_feature_dim, num_classes):

    # Input Layers
    text_input = L.Input(shape=(text_feature_dim,), name="text_features")
    speech_input = L.Input(shape=(speech_feature_dim,), name="speech_features")

    # TEXT BRANCH (LSTM-based)
    text_branch = L.Dense(512, activation="relu")(text_input)
    text_branch = L.Reshape((1, 512))(text_branch)  # Reshape for LSTM
    text_branch = L.LSTM(256, return_sequences=True)(text_branch)
    text_branch = L.LSTM(128, return_sequences=True)(text_branch)  # Keep sequence output
    text_branch = L.BatchNormalization()(text_branch)
    text_branch = L.Dropout(0.3)(text_branch)

    # SPEECH BRANCH (CNN-based)
    speech_branch = L.Dense(2376, activation="relu")(speech_input)  
    speech_branch = L.Reshape((2376, 1))(speech_branch)  # Now reshaping works!
    speech_branch = L.Conv1D(256, kernel_size=3, activation="relu", padding="same")(speech_branch)
    speech_branch = L.MaxPooling1D(pool_size=2)(speech_branch)
    speech_branch = L.Conv1D(128, kernel_size=3, activation="relu", padding="same")(speech_branch)
    speech_branch = L.MaxPooling1D(pool_size=2)(speech_branch)
    speech_branch = L.GlobalAveragePooling1D()(speech_branch)
    speech_branch = L.Reshape((1, 128))(speech_branch)  # Reshape for Cross-Attention
    speech_branch = L.BatchNormalization()(speech_branch)
    speech_branch = L.Dropout(0.3)(speech_branch)

    # **Cross-Attention Layer**
    cross_attention = L.MultiHeadAttention(num_heads=4, key_dim=128)(text_branch, speech_branch)
    fusion = L.Add()([text_branch, cross_attention])  # Residual Connection
    fusion = L.LayerNormalization()(fusion)
    fusion = L.Flatten()(fusion)  # Convert to 2D

    # FINAL CLASSIFICATION LAYERS
    fusion = L.Dense(512, activation="relu")(fusion)
    fusion = L.BatchNormalization()(fusion)
    fusion = L.Dropout(0.3)(fusion)

    fusion = L.Dense(256, activation="relu")(fusion)
    fusion = L.BatchNormalization()(fusion)
    fusion = L.Dropout(0.3)(fusion)

    output = L.Dense(num_classes, activation="softmax")(fusion)

    # Define Model
    fusion_model = tf.keras.Model(inputs=[text_input, speech_input], outputs=output)

    return fusion_model

optimizer = tf.keras.optimizers.Adam(learning_rate = 0.0005)

# Build Fusion Model
fusion_model = build_fusion_model(
    text_feature_dim = 128, 
    speech_feature_dim = 2376, 
    num_classes = 7
)

# Compile Fusion Model
fusion_model.compile(
    optimizer = optimizer,
    loss = "categorical_crossentropy", 
    metrics = ["accuracy"]
)


# Define callbacks
early_stopping = EarlyStopping(
    monitor = "val_loss",  # Track validation loss
    patience = 10,          # Stop after 5 epochs of no improvement
    restore_best_weights = True  # Keep the best model
)

reduce_lr = ReduceLROnPlateau(
    monitor = "val_loss", 
    factor = 0.5,  # Reduce learning rate by 50%
    patience = 5,  # Wait for 3 epochs before reducing LR
    min_lr = 1e-6  # Set a minimum learning rate
)

model_checkpoint = ModelCheckpoint(
    "Models/Fusion/best_fusion_model.h5",
    monitor = "val_loss",
    save_best_only = True,  # Save only the best model
    mode = "min"
)


# Train Fusion Model
fusion_model.fit(
    [text_train_features, speech_train_features], 
    text_train_labels_encoded, 
    epochs = 100, 
    batch_size = 32,
    validation_split = 0.2,
    callbacks = [early_stopping, reduce_lr, model_checkpoint]
)

# Save the model
fusion_model.save("Models/Fusion/fusion_model.h5", save_format = "h5", include_optimizer = True)
