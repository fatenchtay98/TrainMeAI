import cv2
from core.processors.base_processor import BasePoseProcessor
from core.analysis.squat_analysis import analyze_squat_posture

class SquatProcessor(BasePoseProcessor):
    def process(self, frame, pose_model):
        if self.flip_frame:
            frame = cv2.flip(frame, 1)

        results = pose_model.process(frame)
        feedback = "No person detected"

        if results.pose_landmarks:
            feedback, left_angle, right_angle = analyze_squat_posture(
                results.pose_landmarks.landmark, frame.shape)

            # Determine squat state and rep transitions
            if left_angle > 140 and right_angle > 140:
                if self.last_state == 'down':
                    self.rep_count += 1
                    self.last_state = 'up'
            elif left_angle < 90 and right_angle < 90:
                if self.last_state != 'down':
                    self.last_state = 'down'

        frame = self.draw_feedback(frame, feedback)
        return frame, feedback
