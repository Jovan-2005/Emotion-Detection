# Emotion-Based Music Player

This application detects your facial emotion using your webcam and plays music that matches your mood in Spotify.

## Features

- Real-time emotion detection using a pre-trained neural network
- Automatic music selection based on detected emotions
- Direct integration with Spotify to play music
- Fallback to web player and YouTube if needed
- Visual feedback through a live camera feed

## Prerequisites

- Python 3.8 or higher
- Webcam
- Spotify desktop application installed (for best experience)
- Internet connection

## Installation

1. Clone or download this project to your computer
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Make sure your webcam is connected and working
2. Ensure Spotify is installed on your computer (but not necessarily running)
3. Run the application:
   ```
   python main.py
   ```
4. Look at the camera and express the emotion you're feeling
5. The application will detect your emotion, classify it as happy, sad, angry, or neutral
6. It will then open Spotify and play a song that matches your mood

## How It Works

The application uses:
- TensorFlow with a pre-trained model (fer2013_mini_XCEPTION) for emotion detection
- OpenCV for webcam access and face detection
- Pygame for displaying the camera feed
- PyAutoGUI for controlling Spotify
- Direct Spotify integration through URI schemes

## Included Emotions and Music

The application categorizes emotions into:
- Happy (e.g., "Don't Stop Me Now" by Queen)
- Sad (e.g., "Someone Like You" by Adele)
- Angry (e.g., "Till I Collapse" by Eminem)
- Neutral (e.g., "Weightless" by Marconi Union)

## Troubleshooting

- If Spotify doesn't play the song, the application will try multiple methods
- The application will fall back to opening the Spotify web player or YouTube if needed
- Make sure good lighting is available for better emotion detection
- You may need to allow camera access when prompted

## Credits

- Emotion detection model: FER2013 dataset and mini-XCEPTION architecture
- Pre-selected music recommendations curated for each emotion

Enjoy your emotion-based music experience! 