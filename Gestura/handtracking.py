import cv2
import mediapipe as mp
import numpy as np
import pickle

# Load trained sign language model
with open('sign_language_model.pkl', 'rb') as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def normalize_landmarks(landmarks):
    """Normalize hand landmarks relative to the wrist (landmark[0])"""
    if len(landmarks) < 3:
        return landmarks
    base_x, base_y, base_z = landmarks[0], landmarks[1], landmarks[2]
    for i in range(0, len(landmarks), 3):
        landmarks[i] -= base_x
        landmarks[i+1] -= base_y
        landmarks[i+2] -= base_z
    return landmarks

def hand_tracking():
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7
    )
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # Mirror the frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process hand landmarks
            results = hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                    # Extract and normalize landmarks
                    landmark_data = []
                    for lm in hand_landmarks.landmark:
                        landmark_data.extend([lm.x, lm.y, lm.z])
                    landmark_data = normalize_landmarks(landmark_data)
                    
                    # Predict using the model
                    prediction = model.predict(np.array(landmark_data).reshape(1, -1))
                    translated_letter = prediction[0]
                    
                    # Add prediction text to the frame
                    cv2.putText(frame, f"Sign: {translated_letter}", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Convert frame to RGB for Tkinter compatibility
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield frame_rgb
    except GeneratorExit:
        print("Hand tracking stopped.")
    finally:
        cap.release()
        hands.close()
        cv2.destroyAllWindows()