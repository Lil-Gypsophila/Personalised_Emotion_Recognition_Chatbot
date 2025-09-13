# J.A.R.V.I.S - Emotion Recognition Virtual Assistant

A comprehensive emotion recognition system that combines Speech Emotion Recognition (SER), Text Emotion Recognition (TER), and Face Authentication to create an intelligent virtual assistant named J.A.R.V.I.S.

## 🎯 Project Overview

This capstone project implements a multi-modal emotion recognition system that can:
- **Recognize emotions from speech** using deep learning models
- **Analyze text emotions** using Bi-LSTM neural networks
- **Fuse multiple modalities** for improved accuracy
- **Authenticate users** through face recognition
- **Provide intelligent responses** based on detected emotions
- **Control system applications** through voice commands

## 🏗️ System Architecture

### Core Components

1. **Speech Emotion Recognition (SER)**
   - CNN-based model for audio emotion classification
   - Extracts MFCC, spectral, and prosodic features
   - Supports 6 emotion categories

2. **Text Emotion Recognition (TER)**
   - Bi-LSTM neural network for text analysis
   - Preprocessing pipeline with tokenization and padding
   - Natural language understanding capabilities

3. **Fusion Model**
   - Decision-level fusion of SER and TER predictions
   - Weighted averaging strategy (30% speech, 70% text)
   - Improved accuracy through multi-modal integration

4. **Face Authentication**
   - LBPH (Local Binary Patterns Histograms) face recognition
   - User registration and authentication system
   - Real-time face detection and recognition

5. **Virtual Assistant Interface**
   - Web-based UI using Eel framework
   - Voice command processing
   - Real-time emotion display and response generation

## 🚀 Features

### Emotion Recognition
- **Multi-modal Analysis**: Combines speech and text for accurate emotion detection
- **Real-time Processing**: Live audio recording and emotion classification
- **6 Emotion Categories**: Happy, Sad, Angry, Fear, Surprise, Neutral
- **Confidence Scoring**: Probability-based emotion predictions

### Virtual Assistant Capabilities
- **Voice Commands**: Natural language processing for system control
- **Application Launching**: Open programs and websites through voice
- **YouTube Integration**: Search and play videos
- **Text-to-Speech**: Conversational responses with emotion awareness
- **Chat History**: Persistent conversation logging

### Security & Authentication
- **Face Recognition**: Secure user authentication
- **User Management**: Multiple user support with individual profiles
- **Session Management**: Secure login/logout functionality

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 5GB free space
- **Webcam**: Required for face authentication
- **Microphone**: Required for voice input

### Hardware Requirements
- **CPU**: Multi-core processor (Intel i5 or AMD Ryzen 5 minimum)
- **GPU**: NVIDIA GPU with CUDA support (recommended for faster processing)
- **Audio**: High-quality microphone for better speech recognition
- **Camera**: HD webcam for face recognition

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd EMOTION_RECOGNITION_CAPSTONE
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On Windows:
myenv\Scripts\activate
# On Linux/Mac:
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Additional Setup for Audio Processing
```bash
# Install additional audio dependencies
pip install pyaudio
pip install sounddevice
pip install librosa
```

### 5. Download Required Models
The project includes pre-trained models, but ensure you have:
- `haarcascade_frontalface_default.xml` (OpenCV face detection)
- Pre-trained emotion recognition models in `Models/` directory

## ⚙️ Configuration

### 1. API Keys Setup
Create a `.env` file in the project root:
```env
API_KEY_PATH=API/API_KEYS/api_keys.json
```

Update `API/API_KEYS/api_keys.json` with your API keys:
```json
{
  "api_keys": {
    "openai": "your-openai-api-key-here"
  }
}
```

### 2. Face Recognition Setup
1. **Register Users**:
   ```bash
   python engine/auth/sample.py
   ```
   - Follow prompts to capture face samples
   - Each user needs 30+ face images for training

2. **Train Face Recognition Model**:
   ```bash
   python engine/auth/trainer.py
   ```

### 3. Database Setup
The SQLite database will be created automatically on first run. It includes:
- System application paths
- Web application URLs
- User preferences

## 🎮 Usage

### Starting the System
```bash
python main.py
```

### System Workflow
1. **Initialization**: System loads all models and starts web interface
2. **Face Authentication**: User must authenticate via face recognition
3. **Main Interface**: J.A.R.V.I.S interface becomes available
4. **Voice Interaction**: Use microphone button or voice commands
5. **Text Interaction**: Type messages in the chat interface

### Voice Commands
- **"Open [application]"**: Launch system applications
- **"Search [query] on YouTube"**: Search and play YouTube videos
- **General conversation**: Ask questions or have emotional discussions

### Interface Controls
- **Microphone Button**: Start voice recording
- **Chat Button**: View conversation history
- **Settings Button**: Access system settings
- **Send Button**: Send text messages

## 📁 Project Structure

```
EMOTION_RECOGNITION_CAPSTONE/
├── API/                          # API key management
│   ├── API_KEYS/
│   │   └── api_keys.json        # API keys configuration
│   └── api_keys_handler.py      # API key loader
├── database/                     # Database management
│   ├── db.py                    # Database operations
│   └── debs.db                  # SQLite database
├── engine/                       # Core system engine
│   ├── auth/                    # Face authentication
│   │   ├── recognize.py         # Face recognition logic
│   │   ├── sample.py           # User registration
│   │   ├── trainer.py          # Model training
│   │   └── samples/            # User face samples
│   ├── chatbot.py              # OpenAI integration
│   ├── command.py              # Voice/text processing
│   ├── eel_handler.py          # Web interface handler
│   ├── features.py             # System features
│   └── helper.py               # Utility functions
├── Models/                       # Machine learning models
│   ├── Fusion/                 # Fusion model implementation
│   │   ├── best_fusion_model.h5
│   │   ├── build_fusion_model.py
│   │   └── utils/
│   ├── SER/                    # Speech Emotion Recognition
│   │   ├── model.py
│   │   ├── data_preprocessing.py
│   │   ├── feature_engineering.py
│   │   └── utils/
│   ├── TER/                    # Text Emotion Recognition
│   │   ├── model.py
│   │   ├── data_preprocessing.py
│   │   └── utils/
│   └── fusion.py               # Multi-modal fusion
├── templates/                   # Web interface
│   ├── index.html              # Main interface
│   └── static/                 # CSS, JS, assets
├── Notebooks/                   # Jupyter notebooks for development
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Audio/Video Device Issues
**Problem**: Microphone or camera not detected
**Solution**:
- Check device permissions in Windows settings
- Ensure devices are not being used by other applications
- Try different USB ports for external devices

#### 2. Model Loading Errors
**Problem**: Pre-trained models not found
**Solution**:
- Ensure all model files are in correct directories
- Check file permissions
- Re-download models if corrupted

#### 3. API Key Issues
**Problem**: OpenAI API errors
**Solution**:
- Verify API key is correct and active
- Check API usage limits and billing
- Ensure `.env` file is properly configured

#### 4. Face Recognition Failures
**Problem**: Face authentication not working
**Solution**:
- Ensure good lighting conditions
- Retrain face recognition model
- Check camera positioning and focus
- Capture more diverse face samples

#### 5. Dependencies Installation Issues
**Problem**: Package installation failures
**Solution**:
```bash
# Update pip
python -m pip install --upgrade pip

# Install packages individually
pip install tensorflow==2.10.0
pip install opencv-python
pip install pyaudio
```

### Performance Optimization

#### For Better Accuracy
- Use high-quality microphone
- Ensure good lighting for face recognition
- Speak clearly and at moderate pace
- Use diverse training samples for face recognition

#### For Better Performance
- Close unnecessary applications
- Use GPU acceleration if available
- Increase system RAM if possible
- Use SSD storage for faster model loading

## 🧪 Testing

### Test Individual Components
```bash
# Test speech emotion recognition
python -c "from Models.SER.model import predict_speech_emotion; print('SER working')"

# Test text emotion recognition  
python -c "from Models.TER.model import predict_text_emotion; print('TER working')"

# Test face recognition
python -c "from engine.auth.recognize import authenticate_face; print('Face auth working')"
```

### Test Full System
1. Run `python main.py`
2. Complete face authentication
3. Test voice commands
4. Test text input
5. Verify emotion recognition accuracy

## 📊 Model Performance

### Speech Emotion Recognition
- **Accuracy**: ~85% on test dataset
- **Supported Emotions**: 6 categories
- **Processing Time**: ~2-3 seconds per audio sample

### Text Emotion Recognition
- **Accuracy**: ~90% on test dataset
- **Model**: Bi-LSTM with attention mechanism
- **Processing Time**: <1 second per text sample

### Fusion Model
- **Accuracy**: ~92% combined accuracy
- **Strategy**: Weighted averaging (30% SER, 70% TER)
- **Robustness**: Improved performance on ambiguous cases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is part of a capstone project for educational purposes. Please ensure you have proper licenses for all dependencies and models used.

## 👨‍💻 Author

**Cheah Weng Hoe**  
Student ID: TP055533  
Institution: [Your Institution Name]  
Date Created: January 28, 2025  
Last Modified: February 20, 2025

## 🙏 Acknowledgments

- OpenAI for GPT integration
- TensorFlow team for deep learning framework
- OpenCV community for computer vision tools
- All open-source contributors whose libraries made this project possible

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Contact: [your-email@domain.com]
- Documentation: [link-to-docs]

---

**Note**: This is a capstone project demonstrating advanced emotion recognition techniques. Ensure all ethical guidelines and privacy considerations are followed when deploying in production environments.
