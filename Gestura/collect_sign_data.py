import cv2
import mediapipe as mp
import csv

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# Define labels (A-Z)
labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

# Open CSV file
with open('sign_language_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["label"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)] + [f"z{i}" for i in range(21)])

    print("Starting Sign Language Data Collection")
    print("Hold each sign and press 's' to save. The program will automatically switch to the next letter after 5 samples.")

    for label in labels:
        sample_count = 0
        print(f"\nNow signing: '{label}'")

        while sample_count < 5:  # Collect 5 samples per letter
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Extract landmark positions
                    landmark_list = []
                    wrist = hand_landmarks.landmark[0]  # The wrist landmark (used for normalization)

                    for lm in hand_landmarks.landmark:
                        # Normalize by subtracting the wrist position
                        norm_x = lm.x - wrist.x
                        norm_y = lm.y - wrist.y
                        norm_z = lm.z - wrist.z
                        landmark_list.extend([norm_x, norm_y, norm_z])

                cv2.putText(frame, f"Sign '{label}' - Sample {sample_count+1}/5", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Show frame
                cv2.imshow("Sign Data Collection", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):  # Save when 's' is pressed
                    writer.writerow([label] + landmark_list)
                    sample_count += 1
                    print(f"Sample {sample_count}/5 saved for '{label}'")

                elif key == ord('q'):  # Exit if 'q' is pressed
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

    print("\nData collection complete! Exiting...")
    cap.release()
    cv2.destroyAllWindows()
