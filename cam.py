import cv2
import mediapipe as mp

# ====== USTAWIENIA ======
URL = "http://192.168.0.152:4747/video"

# ====== MEDIAPIPE ======
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,       # stream video, nie pojedyncze zdjęcia
    max_num_hands=2,               # maksymalnie 2 dłonie
    min_detection_confidence=0.5,  # próg wykrycia
    min_tracking_confidence=0.5    # próg śledzenia
)

# ====== VIDEO ======
cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Nie udało się otworzyć streamu video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się pobrać klatki.")
        break

    # Odbicie lustrzane - wygodniejsze do pracy
    frame = cv2.flip(frame, 1)

    # OpenCV używa BGR, MediaPipe oczekuje RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Przetwarzanie przez MediaPipe
    results = hands.process(frame_rgb)

    # Jeśli wykryto dłoń/dłonie
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

    cv2.imshow("Hand Landmarks", frame)

    # q = wyjście
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()