import base64
import tempfile
import cv2
import os
import subprocess
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel
from core.utils.pose_loader import get_mediapipe_pose
from core.processors.lateral_raise_processor import LateralRaiseProcessor

router = APIRouter()
pose = get_mediapipe_pose()
session_store = {}  # In-memory session tracker

class FramePayload(BaseModel):
    session_id: str
    image: str  # base64-encoded JPEG image

@router.post("/analyze-video")
async def analyze_lateral_video(video: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_vid:
            temp_vid.write(await video.read())
            input_path = temp_vid.name

        cap = cv2.VideoCapture(input_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

        raw_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        writer = cv2.VideoWriter(raw_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        processor = LateralRaiseProcessor()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frame, _ = processor.process(frame_rgb, pose)
            writer.write(processed_frame[..., ::-1])

        cap.release()
        writer.release()
        os.remove(input_path)

        h264_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_output_path, "-vcodec", "libx264", "-crf", "23", h264_output_path
        ], check=True)

        os.remove(raw_output_path)

        return FileResponse(
            path=h264_output_path,
            media_type="video/mp4",
            filename="lateral_annotated_output.mp4"
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/analyze-frame")
async def analyze_lateral_frame(payload: FramePayload):
    try:
        session_id = payload.session_id

        img_data = base64.b64decode(payload.image)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if session_id not in session_store:
            session_store[session_id] = LateralRaiseProcessor()
        processor = session_store[session_id]

        processed_frame, _ = processor.process(frame_rgb, pose)

        processed_bgr = processed_frame[..., ::-1]
        success, buffer = cv2.imencode('.jpg', processed_bgr)
        if not success:
            raise ValueError("Failed to encode frame")

        return Response(content=buffer.tobytes(), media_type="image/jpeg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
