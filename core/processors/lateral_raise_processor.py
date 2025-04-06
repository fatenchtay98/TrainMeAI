import cv2
from core.processors.base_processor import BasePoseProcessor
from core.analysis.lateral_raise_analysis import analyze_lateral_raise

class LateralRaiseProcessor(BasePoseProcessor):
    def process(self, frame, pose_model):
        if self.flip_frame:
            frame = cv2.flip(frame, 1)

        results = pose_model.process(frame)
        feedback = "No person detected"

        if results.pose_landmarks:
            feedback, left_angle, right_angle = analyze_lateral_raise(
                results.pose_landmarks.landmark, frame.shape)

            # Rep logic (down → up)
            if left_angle > 80 and right_angle > 80:
                if self.last_state == 'down':
                    self.rep_count += 1
                    self.last_state = 'up'
            elif left_angle < 50 and right_angle < 50:
                self.last_state = 'down'

        frame = self.draw_feedback(frame, feedback)
        return frame, feedback
