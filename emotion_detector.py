import cv2
import numpy as np
import pygame
import random
from spotify_integration import play_song

# Define emotion labels
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

def get_emotion():
    """
    Simplified emotion detector that uses basic face detection
    without ML-based emotion recognition.
    """
    print("Initializing webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam. Please check if your webcam is connected and not in use by another application.")
        return "neutral"  # Return default emotion if webcam fails

    # Test webcam read
    ret, test_frame = cap.read()
    if not ret:
        print("Error: Could not read from webcam. Please check your webcam connection.")
        cap.release()
        return "neutral"  # Return default emotion if webcam fails
    print("Webcam initialized successfully!")

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Simplified Emotion Detector")

    # For demo purposes, we'll use a simple UI to select emotions
    # instead of ML-based detection
    detected_emotion = "neutral"  # Default emotion
    selected_emotion = None
    font = pygame.font.SysFont('Arial', 20)
    
    # Define buttons for emotions
    buttons = []
    button_height = 30
    button_width = 100
    button_margin = 10
    button_y = 10
    
    for i, emotion in enumerate(emotion_labels):
        button_x = 10 + i * (button_width + button_margin)
        if button_x + button_width > 640:  # Wrap to next row
            button_y += button_height + button_margin
            button_x = 10 + (i % 5) * (button_width + button_margin)
        
        buttons.append({
            'rect': pygame.Rect(button_x, button_y, button_width, button_height),
            'emotion': emotion,
            'color': (200, 200, 200)
        })

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame from camera. Exiting.")
                break

            # Create a copy for displaying
            display_frame = frame.copy()
                
            # Basic face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw rectangles on detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # In this simplified version, we'll use the selected emotion or a random one
                if selected_emotion:
                    detected_emotion = selected_emotion
                elif random.random() < 0.01:  # Occasionally change emotion randomly
                    detected_emotion = random.choice(emotion_labels)
                
                # Draw text with selected emotion
                cv2.putText(display_frame, detected_emotion, (x, y-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            
            # Convert for pygame display
            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            display_frame = np.swapaxes(display_frame, 0, 1)
            display_surface = pygame.surfarray.make_surface(display_frame)
            
            # Display the frame
            screen.blit(display_surface, (0, 0))
            
            # Draw emotion selection buttons
            for button in buttons:
                pygame.draw.rect(screen, button['color'], button['rect'])
                text = font.render(button['emotion'], True, (0, 0, 0))
                text_rect = text.get_rect(center=button['rect'].center)
                screen.blit(text, text_rect)
            
            # Update display
            pygame.display.update()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(f"Quitting with emotion: {detected_emotion}")
                    return map_emotion(detected_emotion)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if a button was clicked
                    pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button['rect'].collidepoint(pos):
                            selected_emotion = button['emotion']
                            detected_emotion = selected_emotion
                            print(f"Selected emotion: {selected_emotion}")
                            # Highlight the selected button
                            for b in buttons:
                                b['color'] = (200, 200, 200)
                            button['color'] = (100, 255, 100)

    except Exception as e:
        print(f"An error occurred: {e}")
        return map_emotion(detected_emotion)
    finally:
        if cap.isOpened():
            cap.release()
        pygame.quit()

def map_emotion(emotion):
    if emotion in ['happy', 'surprise']:
        return 'happy'
    elif emotion in ['sad', 'fear']:
        return 'sad'
    elif emotion in ['angry']:
        return 'angry'
    else:
        return 'neutral'

if __name__ == "__main__":
    get_emotion()
