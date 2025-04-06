import streamlit as st
import requests
import tempfile

st.title("Lateral Raise Analysis via API")
API_URL = "http://backend:8000/lateral/analyze-video"

with st.form("lateral-upload-form", clear_on_submit=True):
    video_file = st.file_uploader("Upload a lateral raise video", type=["mp4", "avi", "mov"])
    submit = st.form_submit_button("Analyze")

if submit and video_file:
    st.info("Uploading video to backend...")
    files = {"video": (video_file.name, video_file.getvalue(), video_file.type)}

    try:
        response = requests.post(API_URL, files=files)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", mode="wb") as f:
                f.write(response.content)
                saved_path = f.name

            st.success("Analysis complete!")
            st.video(saved_path)

            with open(saved_path, "rb") as f:
                st.download_button("Download Annotated Video", f, file_name="lateral_output.mp4")
        else:
            st.error(f"Backend error: {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")