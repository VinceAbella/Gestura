import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def hand_tracking():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        # Process hand landmarks
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Draw landmarks if hands detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
        cv2.imshow('Basic Sign Language Translator ', frame)

        # Exit on ESC key (key code 27)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()