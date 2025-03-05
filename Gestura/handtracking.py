import cv2
import mediapipe as mp
import numpy as np
import pickle  # Load trained model

# Load trained sign language model
with open('sign_language_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)

def normalize_landmarks(landmarks):
    """ Normalize hand landmarks relative to the wrist (landmark[0]) """
    base_x, base_y, base_z = landmarks[0:3]
    for i in range(0, len(landmarks), 3):
        landmarks[i] -= base_x  # Normalize X
        landmarks[i+1] -= base_y  # Normalize Z
        landmarks[i+2] -= base_z  # Normalize []
    return landmarks

while cap.isOpened():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark positions
            landmark_data = []
            for lm in hand_landmarks.landmark:
                landmark_data.extend([lm.x, lm.y, lm.z])

            # Normalize landmarks before prediction
            landmark_data = normalize_landmarks(landmark_data)

            # Convert to NumPy array for model input
            landmark_data = np.array(landmark_data).reshape(1, -1)

            # Predict sign language letter
            prediction = model.predict(landmark_data)
            translated_letter = prediction[0]

            # Display result
            cv2.putText(frame, f"Sign: {translated_letter}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Sign Language Translator", frame)

    # Exit with ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
