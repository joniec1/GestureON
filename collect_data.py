import cv2
import mediapipe as mp
import csv
import os

URL = "http://192.168.0.152:4747/video"
LABEL = "thumb_up"   # <- zmieniasz zależnie od gestu

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Nie udało się otworzyć streamu video.")
    exit()

os.makedirs("data", exist_ok=True)
file_path = f"data/{LABEL}.csv"

with open(file_path, mode="a", newline="") as f:
    writer = csv.writer(f)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nie udało się pobrać klatki.")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        row = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                row = []
                for lm in hand_landmarks.landmark:
                    row.append(lm.x)
                    row.append(lm.y)

        cv2.putText(frame, f"Label: {LABEL}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "s = save, q = quit", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.imshow("Collect Data", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            if row is not None and len(row) == 42:
                writer.writerow(row)
                print("Zapisano próbkę.")
            else:
                print("Brak poprawnie wykrytej dłoni.")

        elif key == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
hands.close()