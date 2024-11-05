import cv2
import time
from collections import Counter
from deepface import DeepFace
import streamlit as st
import numpy as np
import urllib.parse 
# Streamlit App Setup
st.title("Real-Time Emotion Detection with Song Recommendations")
st.markdown("This app captures emotions over a few seconds, identifies the dominant emotion, and recommends songs.")

# Initialize face cascade for detection
facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Set up Streamlit layout
frame_placeholder = st.empty()  # Placeholder for video frame
emotion_placeholder = st.empty()  # Placeholder for current emotion text
capture_status = st.empty()       # Placeholder for capture status

# Set duration for capturing emotions
capture_duration = 4  # Duration in seconds to capture emotions

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
if not cap.isOpened():
    st.error("Cannot open webcam")
    st.stop()

# Define a function to capture emotions
def capture_emotions():
    start_time = time.time()
    emotion_counts = Counter()
    
    # Notify user of capture
    capture_status.info("Capturing emotions...")

    # Capture emotions over the specified duration
    while (time.time() - start_time) < capture_duration:
        ret, frame = cap.read()
        if not ret or frame is None:
            frame_placeholder.image(np.zeros((480, 640, 3), np.uint8), channels="BGR")  # Display blank frame
            emotion_placeholder.text("No video feed detected.")
            continue

        # Process frame for emotion detection
        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
            if isinstance(result, list):
                emotion = result[0]['dominant_emotion']
            else:
                emotion = result['dominant_emotion']
            emotion_counts[emotion] += 1
        except Exception as e:
            emotion = "No Face Detected"
            print("Error during face analysis:", e)

        # Convert frame to RGB (for display in Streamlit)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display frame and emotion in Streamlit
        frame_placeholder.image(frame_rgb, channels="RGB", width=640)
        #emotion_placeholder.text(f"Current Emotion: {emotion}")

    # Determine the dominant emotion after capture duration
    capture_status.empty()  # Clear the capturing message
    if emotion_counts:
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        
        
        emotion_string=""
        # Assuming emotions is a dictionary with emotion counts
        emotion_counts_unique = emotion_counts.keys()  # Get the unique emotions from the keys
        emotion_string = ", ".join(emotion_counts_unique)  # Join unique emotions with a comma

        st.write("The emotions captured in last few seconds is:\n"+emotion_string)
        st.write(f"**Dominant Emotion:** {dominant_emotion}")
        search_term = f"{dominant_emotion} songs"
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_term)}"
        st.link_button("Search songs", search_url)
            
    else:
        st.write("No emotions detected.")

# Initial capture and re-capture option
if st.button("Capture Emotions"):
    capture_emotions()

# Release resources when the app stops
cap.release()
