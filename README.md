# Music by Mood

## Overview
Music by Mood is a Streamlit-based web application that captures emotions over a few seconds using your webcam, identifies the dominant emotion, and recommends songs based on the detected mood.

## Features
- Captures emotions using OpenCV and DeepFace
- Analyzes emotions over a set duration (default: 5 seconds)
- Identifies the dominant emotion from the captured frames
- Displays the frame corresponding to the dominant emotion
- Provides a YouTube search link for songs matching the dominant emotion

## Requirements
To run this application, ensure you have the following installed:

- Python 3.7+
- Streamlit
- OpenCV (cv2)
- NumPy
- DeepFace
- Matplotlib

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/music-by-mood.git
   cd music-by-mood
   ```
2. Create and activate a virtual environment:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Allow webcam access when prompted.
3. Click the "Start Video Capture" button to begin emotion analysis.
4. Wait for the analysis to complete and view the detected emotions.
5. Click the provided YouTube link to explore mood-based music recommendations.

## Notes
- Ensure your webcam is functional and enabled for the browser.
- This application requires an internet connection for YouTube search results.
- Emotion detection accuracy depends on lighting and face visibility.



## Acknowledgments
- [Streamlit](https://streamlit.io/)
- [DeepFace](https://github.com/serengil/deepface)
- OpenCV for image processing

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---
Enjoy using Music by Mood! 🎵

