import cv2
import mediapipe as mp
import numpy as np
import joblib

URL = "http://192.168.0.152:4747/video"

# Wczytanie modelu
model = joblib.load("model.pkl")

# Mapowanie indeksów klas na nazwy
labels = ["open_hand", "fist", "thumbs_up"]

# MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Video stream
cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Nie udało się otworzyć streamu video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się pobrać klatki.")
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    predicted_label = "No hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # rysowanie landmarków
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # przygotowanie danych wejściowych
            row = []
            for lm in hand_landmarks.landmark:
                row.append(lm.x)
                row.append(lm.y)

            if len(row) == 42:
                X = np.array(row).reshape(1, -1)
                pred = model.predict(X)[0]
                predicted_label = labels[pred]

    # Wyświetlanie wyniku
    cv2.putText(
        frame,
        f"Prediction: {predicted_label}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Live Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()