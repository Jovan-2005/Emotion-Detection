from emotion_detector import get_emotion
from spotify_integration import play_song

def main():
    print("Starting the Emotion Detector...")

    emotion = get_emotion()
    print(f"Detected emotion: {emotion}")

    print("Opening Spotify with songs matching your emotion...")
    result = play_song(emotion)
    
    if result:
        print(result)
    else:
        print("Could not open Spotify. Please try manually opening Spotify and searching for songs matching your emotion.")

if __name__ == "__main__":
    main()
