from core.utils.geometry_utils import calculate_angle

def analyze_squat_posture(landmarks, frame_shape):
    """
    Analyze squat posture based on hip-knee-ankle angles.
    Returns feedback and joint angles.
    """
    image_height, image_width = frame_shape[:2]

    # Get keypoints (left/right hip, knee, ankle)
    lh, lk, la = landmarks[23], landmarks[25], landmarks[27]
    rh, rk, ra = landmarks[24], landmarks[26], landmarks[28]

    # Convert normalized coords to pixel
    def to_px(landmark):
        return int(landmark.x * image_width), int(landmark.y * image_height)

    left_angle = calculate_angle(to_px(lh), to_px(lk), to_px(la))
    right_angle = calculate_angle(to_px(rh), to_px(rk), to_px(ra))

    feedback = "Go lower" if left_angle > 140 and right_angle > 140 else "Good squat"
    return feedback, left_angle, right_angle
