import cv2
import mediapipe as mp
import numpy as np
import pickle
import os

# Load trained sign language model
with open('sign_language_model.pkl', 'rb') as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class ImageOverlay:
    def __init__(self, image_path):
        self.reference_img = self._load_reference_image(image_path)
    
    def _load_reference_image(self, image_path):
        """Load and prepare the reference image."""
        print(f"Looking for reference image at: {image_path}")
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            image = cv2.resize(image, (425, 367))
            print("Reference image loaded successfully")
            return image
        print(f"Reference image not found: {image_path}")
        return None
    
    def apply_overlay(self, frame):
        """Overlay the reference image on the frame."""
        if self.reference_img is None:
            return frame
        
        height, width = frame.shape[:2]
        ref_h, ref_w = self.reference_img.shape[:2]
        x_offset = width - ref_w - 10
        y_offset = 10
    
        roi = frame[y_offset:y_offset+ref_h, x_offset:x_offset+ref_w]
        if roi.shape[0] > 0 and roi.shape[1] > 0:
            alpha = 0.7
            frame[y_offset:y_offset+ref_h, x_offset:x_offset+ref_w] = \
                cv2.addWeighted(self.reference_img, alpha, roi, 1-alpha, 0)
        return frame

class LandmarkNormalizer:
    @staticmethod
    def normalize(landmarks):
        """Normalize hand landmarks relative to the wrist."""
        if len(landmarks) < 3:
            return landmarks
        
        base_x, base_y, base_z = landmarks[0], landmarks[1], landmarks[2]
        normalized = []
        for i in range(0, len(landmarks), 3):
            normalized.extend([
                landmarks[i] - base_x,
                landmarks[i+1] - base_y,
                landmarks[i+2] - base_z
            ])
        return normalized

class HandTracker:
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_overlay = ImageOverlay(
            os.path.join(script_dir, "sign_references.jpg")
        )
        self.landmark_normalizer = LandmarkNormalizer()
    
    def start_tracking(self):
        """Generator function to yield processed frames."""
        cap = cv2.VideoCapture(0)
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                frame = self.image_overlay.apply_overlay(frame)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self._draw_landmarks(frame, hand_landmarks)
                        self._process_prediction(frame, hand_landmarks)
                
                yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except GeneratorExit:
            print("Hand tracking stopped.")
        finally:
            cap.release()
            self.hands.close()
            cv2.destroyAllWindows()
    
    def _draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame."""
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )
    
    def _process_prediction(self, frame, hand_landmarks):
        """Process landmarks and display prediction."""
        landmark_data = []
        for lm in hand_landmarks.landmark:
            landmark_data.extend([lm.x, lm.y, lm.z])
        normalized_data = self.landmark_normalizer.normalize(landmark_data)
        prediction = model.predict(np.array(normalized_data).reshape(1, -1))
        cv2.putText(frame, f"Sign: {prediction[0]}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def hand_tracking():
    """Interface function to maintain compatibility with buttons.py."""
    tracker = HandTracker()
    return tracker.start_tracking()