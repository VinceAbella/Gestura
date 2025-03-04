import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands()

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    # Process hand landmarks
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # Draw landmarks if hands detected
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
    
    cv2.imshow('Basic Sign Language Translator ', frame)

     # Exit on ESC key (key code 27)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()