import cv2
import mediapipe as mp
import numpy as np
import pickle
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load trained sign language model
with open('sign_language_model.pkl', 'rb') as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def load_reference_image(image_path):
    """Load and prepare the reference image."""
    print(f"Looking for reference image at: {image_path}")
    if os.path.exists(image_path):
        image = cv2.imread(image_path)
        # Resize reference image to a reasonable size for overlay
        image = cv2.resize(image, (200, 300))
        print(f"Reference image found and loaded successfully")
        return image
    else:
        print(f"Reference image not found: {image_path}")
        return None

def overlay_reference_image(frame, reference_img):
    """Overlay the reference image on the frame."""
    if reference_img is None:
        return frame
        
    # Original frame dimensions
    height, width = frame.shape[:2]
    ref_h, ref_w = reference_img.shape[:2]
    
    # Position in top-right corner with padding
    x_offset = width - ref_w - 10
    y_offset = 10
    
    # Create a region of interest
    roi = frame[y_offset:y_offset+ref_h, x_offset:x_offset+ref_w]
    
    # Check if ROI is valid (within frame boundaries)
    if roi.shape[0] > 0 and roi.shape[1] > 0:
        # Overlay the reference image
        # Blend with 70% reference image, 30% original frame
        alpha = 0.7
        frame[y_offset:y_offset+ref_h, x_offset:x_offset+ref_w] = \
            cv2.addWeighted(reference_img, alpha, roi, 1-alpha, 0)
            
    return frame

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
    
    # Load reference image
    reference_img_path = os.path.join(script_dir, "sign_references.jpg")
    reference_img = load_reference_image(reference_img_path)
    
    cap = cv2.VideoCapture(0)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # Mirror the frame
            
            # Overlay reference image
            frame = overlay_reference_image(frame, reference_img)
            
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