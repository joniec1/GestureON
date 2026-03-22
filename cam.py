import cv2
import mediapipe as mp

print(mp)

# Moduły MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Konfiguracja detektora dłoni
hands = mp_hands.Hands(
    static_image_mode=False,      # pracujemy na strumieniu z kamery
    max_num_hands=2,              # maksymalnie 2 dłonie
    min_detection_confidence=0.5, # pewność wykrycia dłoni
    min_tracking_confidence=0.5   # pewność śledzenia w kolejnych klatkach
)

# Kamera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Nie udało się otworzyć kamery.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się pobrać klatki z kamery.")
        break

    # Odbicie lustrzane - wygodniejsze do pracy
    frame = cv2.flip(frame, 1)

    # OpenCV czyta w BGR, MediaPipe oczekuje RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Przetwarzanie obrazu
    results = hands.process(frame_rgb)

    # Jeśli wykryto dłonie
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Rysowanie punktów i połączeń
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

    cv2.imshow("MediaPipe Hands", frame)

    # Wyjście po naciśnięciu q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()