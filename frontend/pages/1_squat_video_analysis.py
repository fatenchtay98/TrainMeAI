import streamlit as st
import requests
import tempfile

st.title("AI Fitness Analysis Squat")

API_URL = "http://backend:8000/squat/analyze-video"

with st.form("squat-upload-form", clear_on_submit=True):
    video_file = st.file_uploader("Upload a squat video", type=["mp4", "avi", "mov"])
    submit = st.form_submit_button("Analyze")

if submit and video_file:
    st.info("Uploading video to backend...")
    files = {"video": (video_file.name, video_file.getvalue(), video_file.type)}

    try:
        response = requests.post(API_URL, files=files)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", mode="wb") as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name

            st.success("Processed video received.")
            st.video(temp_path)

            with open(temp_path, "rb") as f:
                st.download_button("Download Processed Video", f, file_name="squat_analysis.mp4")
        else:
            st.error(f"Backend error: {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error(f"Could not connect to backend API: {e}")