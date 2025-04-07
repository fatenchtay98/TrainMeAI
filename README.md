
# AI Pose Fitness Tracker

**AI-Pose-Fitness-Tracker** is a real-time, AI-powered fitness tracking system designed to help users monitor and improve their exercise form using pose estimation. The app supports both video uploads and live webcam streams, allowing users to receive immediate feedback on movements like lateral raises and squats — with automatic rep counting and annotated feedback.

This project leverages **MediaPipe**, a powerful open-source framework developed by Google for building multimodal ML pipelines. MediaPipe Pose is used to estimate 33 human body keypoints in real time with high accuracy, enabling form detection and rep counting in exercises.

# Features

- Lateral Raise Tracking via video upload or live stream
- Squats Tracking via video upload or live stream
- Real-time Pose Estimation using MediaPipe
- Annotated video overlays for visual guidance
- Repetition counting with form feedback
- Downloadable processed videos after analysis


# Local Setup

### Clone the Repo
git clone https://github.com/Jenny926804/AI-Pose-Fitness-Tracker.git
cd AI-Fitness-Trainer

### Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

### Running the app
sudo docker-compose up --build

Once running, open your browser and visit:
📍 http://localhost:8501

From the sidebar in Streamlit, choose:
    - Upload Squat Video
    - Upload Lateral Raise Video
    - Live Tracker for Real-Time Analysis

Then:
1 - Upload or activate your camera
2 - Perform your reps
3 - Watch real-time feedback on your posture and movement
4 - Download your annotated workout video for review