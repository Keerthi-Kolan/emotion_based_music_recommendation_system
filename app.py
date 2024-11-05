import streamlit as st
import numpy as np
import urllib.parse
import cv2
import time
from collections import Counter
from deepface import DeepFace
import matplotlib.pyplot as plt

# Streamlit App Setup
st.title("Music by Mood")
st.markdown("This app captures emotions over a few seconds, identifies the dominant emotion, and recommends songs.")

# Set duration for capturing emotions
capture_duration = 5  # Duration in seconds to capture emotions

# Define a function to analyze emotions from the captured frames
def capture_emotions(frames):
    emotion_counts = Counter()
    unique_frames = {}  # Dictionary to store unique frames for each emotion

    # Process each frame for emotion detection
    for frame in frames:
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(result, list):
                emotion = result[0]['dominant_emotion']
            else:
                emotion = result['dominant_emotion']
            
            emotion_counts[emotion] += 1
            
            # Store the first frame corresponding to each unique emotion
            if emotion not in unique_frames:
                unique_frames[emotion] = frame
            
        except Exception as e:
            print("Error during face analysis:", e)

    return emotion_counts, unique_frames

# Function to display the dominant emotion frame
def display_dominant_emotion_frame(unique_frames, dominant_emotion):
    if dominant_emotion in unique_frames:
        frame = unique_frames[dominant_emotion]
        # Convert the frame to RGB format for display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption=f"Dominant Emotion: {dominant_emotion}", use_column_width=True)

# Start the video capture process
if st.button("Start Video Capture"):
    
    # Create a list to store frames
    frames = []
    end_time = time.time() + capture_duration

    # Use OpenCV to capture video from webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Cannot open webcam")
        st.stop()

    # Use a spinner while capturing frames
    with st.spinner("Capturing your emotions, please wait..."):
        # Capture frames for the duration
        while time.time() < end_time:
            ret, frame = cap.read()
            if ret:
                # Store the frame
                frames.append(frame)

    cap.release()  # Release the webcam

    # Use a spinner to show that the app is processing
    with st.spinner("Analyzing your emotions, please wait..."):
        # Analyze the captured frames for emotions
        emotion_counts, unique_frames = capture_emotions(frames)

    # Determine the dominant emotion
    if emotion_counts:
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        
        emotion_string = ", ".join(emotion_counts.keys())  # Join unique emotions with a comma

        # Display the emotions detected
        st.write("The emotions captured in the last few seconds are:\n" + emotion_string)
        st.write(f"**Dominant Emotion:** {dominant_emotion}")

        # Display only the frame for the dominant emotion
        display_dominant_emotion_frame(unique_frames, dominant_emotion)

        search_term = f"{dominant_emotion} songs"
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_term)}"
        st.markdown(f"[Search for {dominant_emotion} songs on YouTube]({search_url})")
    else:
        st.write("No emotions detected.")

# Inform user about webcam permissions
st.write("Please allow access to your webcam in the browser for this application to work.")
