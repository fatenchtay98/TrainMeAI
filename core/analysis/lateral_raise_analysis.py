from core.utils.geometry_utils import calculate_angle

def analyze_lateral_raise(landmarks, frame_shape):
    """
    Analyze lateral raise based on elbow–shoulder–hip angle (upper arm lift).
    Returns feedback and joint angles.
    """
    h, w = frame_shape[:2]

    # Landmarks: shoulder = 11/12, elbow = 13/14, hip = 23/24
    le, ls, lh = landmarks[13], landmarks[11], landmarks[23]  # Left arm
    re, rs, rh = landmarks[14], landmarks[12], landmarks[24]  # Right arm

    def to_px(lm): return int(lm.x * w), int(lm.y * h)

    left_angle = calculate_angle(to_px(le), to_px(ls), to_px(lh))   # elbow–shoulder–hip
    right_angle = calculate_angle(to_px(re), to_px(rs), to_px(rh))

    # Feedback logic
    if left_angle > 80 and right_angle > 80:
        feedback = "Good form"
    elif left_angle < 45 and right_angle < 45:
        feedback = "Arms lowered"
    else:
        feedback = "Raise higher"

    return feedback, left_angle, right_angle
