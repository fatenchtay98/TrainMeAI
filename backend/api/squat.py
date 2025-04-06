from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, Response
import tempfile
import cv2
import subprocess
import numpy as np
import os
from core.utils.pose_loader import get_mediapipe_pose
from core.processors.squat_processor import SquatProcessor

router = APIRouter()
pose = get_mediapipe_pose()
squat_processor = SquatProcessor()

@router.post("/analyze-video")
async def analyze_squat(video: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_vid:
            temp_vid.write(await video.read())
            temp_input_path = temp_vid.name

        cap = cv2.VideoCapture(temp_input_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

        raw_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        writer = cv2.VideoWriter(raw_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frame, _ = squat_processor.process(frame_rgb, pose)
            writer.write(processed_frame[..., ::-1])

        cap.release()
        writer.release()
        os.remove(temp_input_path)

        h264_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_output_path, "-vcodec", "libx264", "-crf", "23", h264_output_path
        ], check=True)

        os.remove(raw_output_path)

        return FileResponse(
            path=h264_output_path,
            media_type="video/mp4",
            filename="squat_processed.mp4"
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})