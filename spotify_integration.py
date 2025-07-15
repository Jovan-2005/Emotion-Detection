import webbrowser
import time
import os
import subprocess
import urllib.parse
import random
import pyautogui
import requests
from urllib.error import URLError

# Define emotion-based song recommendations with specific Spotify URIs where possible
EMOTION_SONGS = {
    "happy": [
        {"name": "Happy", "artist": "Pharrell Williams", "uri": "spotify:track:60nZcImufyMA1MKQY3dcCH"},
        {"name": "Can't Stop the Feeling", "artist": "Justin Timberlake", "uri": "spotify:track:1WkMMavIMc4JZ8cfMmxHkI"},
        {"name": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "uri": "spotify:track:32OlwWuMpZ6b0aN2RZOeMS"},
        {"name": "Good as Hell", "artist": "Lizzo", "uri": "spotify:track:3Yh9lZcWyKrK9GjbhuS0hT"},
        {"name": "Walking on Sunshine", "artist": "Katrina & The Waves", "uri": "spotify:track:05wIrZSwuaVWhcv5FfqeH0"}
    ],
    "sad": [
        {"name": "Someone Like You", "artist": "Adele", "uri": "spotify:track:4kflIGfjdZJW4ot2ioixFB"},
        {"name": "Say You Love Me", "artist": "Jessie Ware", "uri": "spotify:track:05WmIQNZ2YmjDzw3Ib4DVf"},
        {"name": "Skinny Love", "artist": "Bon Iver", "uri": "spotify:track:2QV9iVmFKJmG5XzYeRoQjE"},
        {"name": "when the party's over", "artist": "Billie Eilish", "uri": "spotify:track:43zdsphuZLzwA9k4DJhU0I"},
        {"name": "Fix You", "artist": "Coldplay", "uri": "spotify:track:7LVHVU3tWfcxj5aiPFEW4Q"}
    ],
    "angry": [
        {"name": "Till I Collapse", "artist": "Eminem", "uri": "spotify:track:6yr8GiTHWvFfi4bGq2nK0c"},
        {"name": "HUMBLE.", "artist": "Kendrick Lamar", "uri": "spotify:track:7KXjTSCq5nL1LoYtL7XAwS"},
        {"name": "Killing In The Name", "artist": "Rage Against The Machine", "uri": "spotify:track:59WN2psjkt1tyaxjspN8fp"},
        {"name": "Survival", "artist": "Eminem", "uri": "spotify:track:3RS0uWR8l1LHHlO5UbN2VD"},
        {"name": "Not Afraid", "artist": "Eminem", "uri": "spotify:track:4Jb7zUPVKkUmODI7eiPzYR"}
    ],
    "neutral": [
        {"name": "Weightless", "artist": "Marconi Union", "uri": "spotify:track:4e5RyeP8ZFn1UUkITRQ2Uu"},
        {"name": "Watermark", "artist": "Enya", "uri": "spotify:track:65qrLHpDe3zBULB5ucQrGI"},
        {"name": "Pure Shores", "artist": "All Saints", "uri": "spotify:track:7rRAPEBuDjG8I5JYAFtVbU"},
        {"name": "Please Don't Go", "artist": "Barcelona", "uri": "spotify:track:2qdCXhwmcORQiH1aBqx61A"},
        {"name": "Chasing Cars", "artist": "Snow Patrol", "uri": "spotify:track:0snQkGI5qnAmohLE7jTsTn"}
    ]
}

def ensure_spotify_open():
    """Launch Spotify app and ensure it's running"""
    try:
        # Check if Spotify is already running
        if os.name == 'nt':  # Windows
            try:
                output = subprocess.check_output('tasklist /FI "IMAGENAME eq spotify.exe"', shell=True)
                if b"spotify.exe" in output:
                    print("Spotify is already running")
                    return True
            except subprocess.CalledProcessError:
                pass
        
        # Try to open Spotify using the protocol
        print("Attempting to open Spotify...")
        # First, try to open desktop app with direct protocol
        webbrowser.open("spotify:")
        
        # Wait for Spotify to open with a timeout
        for i in range(20):  # Try for 20 seconds, increased from 10
            time.sleep(1)
            if os.name == 'nt':
                try:
                    output = subprocess.check_output('tasklist /FI "IMAGENAME eq spotify.exe"', shell=True)
                    if b"spotify.exe" in output:
                        print("Spotify successfully launched")
                        return True
                except subprocess.CalledProcessError:
                    continue
        
        # If we couldn't verify desktop app, try web player
        print("Couldn't verify desktop app, trying Spotify Web Player...")
        webbrowser.open("https://open.spotify.com")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error opening Spotify: {e}")
        return False

def verify_spotify_uri(uri):
    """Verify if a Spotify URI is valid by checking the web API"""
    try:
        track_id = uri.split(':')[-1]
        response = requests.head(f"https://open.spotify.com/track/{track_id}")
        return response.status_code == 200
    except Exception:
        return False

def force_play():
    """Force play using keyboard shortcuts in various configurations"""
    try:
        # Bring focus to Spotify with Alt+Tab
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        
        # Try standard play button
        pyautogui.press('space')
        time.sleep(0.5)
        
        # Try alternate play command
        pyautogui.press('playpause')
        time.sleep(0.5)
        
        # For web player, try clicking the big play button (approximate center of screen)
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(0.5)
        
        # Try media keys if available
        pyautogui.press('playpause')
        
        return True
    except Exception as e:
        print(f"Keyboard control failed: {e}")
        return False

def play_spotify_track(track_name, artist_name, track_uri=None):
    """Play a specific track on Spotify with enhanced reliability"""
    methods_tried = []
    
    try:
        if track_uri and verify_spotify_uri(track_uri):
            # First try direct desktop app method - most reliable
            track_id = track_uri.split(':')[-1]
            
            # Method 1: Use spotify:// protocol with direct play command
            methods_tried.append("spotify_protocol_play")
            direct_play_uri = f"spotify://track/{track_id}/play"
            print(f"Attempting direct protocol play: {direct_play_uri}")
            webbrowser.open(direct_play_uri)
            time.sleep(5)  # Wait longer to ensure it loads
            
            # Method 2: Use proper spotify: URI format with play action 
            methods_tried.append("direct_play_uri")
            direct_play_uri = f"spotify:track:{track_id}:play"
            print(f"Attempting direct play URI: {direct_play_uri}")
            webbrowser.open(direct_play_uri)
            time.sleep(5)
            
            # Method 3: Try opening the track in desktop app first, then force play
            methods_tried.append("standard_uri_then_play")
            print(f"Attempting standard URI: {track_uri}")
            webbrowser.open(track_uri)
            time.sleep(4)
            force_play()
            
            # Method 4: Try web player with autoplay - this often works better for new songs
            methods_tried.append("web_player_direct")
            web_play_url = f"https://open.spotify.com/track/{track_id}?autoplay=true"
            print(f"Attempting web player direct play: {web_play_url}")
            webbrowser.open(web_play_url)
            time.sleep(4)
            
            # Try clicking play in web player
            try:
                # Try to click the big green play button in web player
                screen_width, screen_height = pyautogui.size()
                # The big play button is usually in the bottom left area
                pyautogui.click(screen_width // 4, screen_height - 100)
                time.sleep(1)
            except Exception as e:
                print(f"Web player click failed: {e}")
        
        # Method 5: Last resort - use Spotify's search and try to find and play
        search_query = f"{track_name} {artist_name}"
        methods_tried.append("search_query")
        if os.name == 'nt':  # Windows
            try:
                # Direct command to Spotify app to search and play
                encoded_query = urllib.parse.quote(search_query)
                search_cmd = f'start spotify:search:{encoded_query}'
                print(f"Running direct search command: {search_cmd}")
                subprocess.run(search_cmd, shell=True)
                time.sleep(4)
                
                # Try to tab to first result and play it
                pyautogui.press('tab', presses=5, interval=0.2)  # Navigate to first result
                pyautogui.press('enter')  # Select it
                time.sleep(2)
                pyautogui.press('space')  # Play it
            except Exception as e:
                print(f"Direct search command failed: {e}")
        
        print(f"Attempted methods: {', '.join(methods_tried)}")
        return True
    
    except Exception as e:
        print(f"Error playing track: {e}")
        print(f"Failed methods: {', '.join(methods_tried)}")
        return False

def play_song(emotion):
    """Select and play a song based on the detected emotion with enhanced error handling"""
    try:
        # Validate and normalize emotion
        emotion = emotion.lower().strip()
        if emotion not in EMOTION_SONGS:
            print(f"Unknown emotion: {emotion}, defaulting to neutral")
            emotion = "neutral"
        
        # Get available songs for the emotion
        songs = EMOTION_SONGS[emotion]
        if not songs:
            print("No songs available for this emotion, using neutral")
            songs = EMOTION_SONGS["neutral"]
        
        # Select and try songs until one works
        random.shuffle(songs)  # Randomize the order
        errors = []
        
        # Try to stop any currently playing music first
        try:
            pyautogui.hotkey('alt', 'tab')  # Focus Spotify if it's open
            time.sleep(1)
            pyautogui.press('space')  # Pause any current playback
            time.sleep(1)
        except Exception:
            pass  # Ignore if this fails
        
        for song in songs[:3]:  # Try up to 3 songs
            track_name = song["name"]
            artist_name = song["artist"]
            track_uri = song.get("uri")
            
            print(f"Attempting to play: {track_name} by {artist_name}")
            
            # Ensure Spotify is open
            if not ensure_spotify_open():
                error_msg = "Could not open Spotify. Please ensure it's installed."
                errors.append(error_msg)
                continue
            
            # Try to play the song
            if play_spotify_track(track_name, artist_name, track_uri):
                print("Song should now be playing. Confirming playback...")
                # One final attempt to ensure playback
                time.sleep(2)
                force_play()
                return f"Now playing: {track_name} by {artist_name}"
            
            errors.append(f"Failed to play: {track_name} by {artist_name}")
        
        # If all attempts failed
        error_summary = "\n".join(errors)
        return f"Could not play any songs for {emotion} emotion.\nErrors:\n{error_summary}"
            
    except Exception as e:
        print(f"Critical error in play_song: {e}")
        return "Error playing song"

if __name__ == "__main__":
    # Example usage
    emotion = input("Enter an emotion (happy, sad, angry, or neutral): ")
    result = play_song(emotion)
    print(result)

