import streamlit as st
import av
import cv2
import numpy as np
import requests
import base64
import uuid
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoProcessorBase

API_ENDPOINTS = {
    "Squat": "http://backend:8000/squat/analyze-frame",
    "Lateral Raise": "http://backend:8000/lateral/analyze-frame"
}

st.title("📡 Live Pose Analysis via API")
exercise = st.selectbox("Choose Exercise", list(API_ENDPOINTS.keys()))
api_url = API_ENDPOINTS[exercise]
frame_interval = 10

class PoseAnalyzerViaAPI(VideoProcessorBase):
    def __init__(self, api_url):
        self.frame_count = 0
        self.last_response = None
        self.session_id = str(uuid.uuid4())
        self.api_url = api_url
        self.session = requests.Session()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        self.frame_count += 1
        img = frame.to_ndarray(format="bgr24")
        resized = cv2.resize(img, (320, 240))

        if self.frame_count % frame_interval == 0:
            _, img_encoded = cv2.imencode(".jpg", resized, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            img_base64 = base64.b64encode(img_encoded).decode("utf-8")
            payload = {"session_id": self.session_id, "image": img_base64}

            try:
                response = self.session.post(self.api_url, json=payload, timeout=5)
                if response.status_code == 200:
                    self.last_response = response.content
            except Exception as e:
                print(f"❌ Request error: {e}")

        if self.last_response:
            decoded = cv2.imdecode(np.frombuffer(self.last_response, np.uint8), cv2.IMREAD_COLOR)
            if decoded is not None:
                return av.VideoFrame.from_ndarray(decoded, format="bgr24")

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="api-live-analysis",
    video_processor_factory=lambda: PoseAnalyzerViaAPI(api_url),
    rtc_configuration=RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }),
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
