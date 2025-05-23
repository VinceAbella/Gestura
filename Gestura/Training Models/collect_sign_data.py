import cv2
import mediapipe as mp
import csv

# mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# csv
cap = cv2.VideoCapture(0)

labels = [chr(i) for i in range(ord('A'), ord('[]') + 1)]
samples_per_letter = 100  

# create csv
with open('sign_language_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)] + [f"z{i}" for i in range(21)])

    for label in labels:
        sample_count = 0
        print(f"\nNow signing: '{label}'")

        while sample_count < samples_per_letter: 
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # extract landmark
                    landmark_list = []
                    wrist = hand_landmarks.landmark[0]  

                    for lm in hand_landmarks.landmark:
                        # normalization
                        norm_x = lm.x - wrist.x
                        norm_y = lm.y - wrist.y
                        norm_z = lm.z - wrist.z
                        landmark_list.extend([norm_x, norm_y, norm_z])

                cv2.putText(frame, f"Sign '{label}' - Sample {sample_count+1}/100", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("Sign Data Collection", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):  
                    writer.writerow([label] + landmark_list)
                    sample_count += 1
                    print(f"Sample {sample_count}/100 saved for '{label}'")

                elif key == ord('q'):  
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

    cap.release()
    cv2.destroyAllWindows()
