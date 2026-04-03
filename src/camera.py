from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import mediapipe as mp
import time

from mediapipe.tasks.python import vision, BaseOptions


class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(object)   # frame do GUI
    data_signal = pyqtSignal(object)            # list[float] | None

    def __init__(self, url: str, model: str):
        super().__init__()
        self.url = url
        self._running = True
        self.model_path = model

        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            num_hands=1,
            running_mode=vision.RunningMode.VIDEO
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def run(self):
        cap = cv2.VideoCapture(self.url)

        while self._running:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            timestamp = int(time.perf_counter() * 1000)
            result = self.detector.detect_for_video(mp_image, timestamp)

            landmarks_row = self.extract_landmarks(result)
            self.data_signal.emit(landmarks_row)

            self.draw_landmarks(frame, result)
            self.change_pixmap_signal.emit(frame)

        cap.release()

    def stop(self):
        self._running = False

    @staticmethod
    def extract_landmarks(result) -> list[float] | None:
        """
        Zwraca listę 42 wartości:
        [x1, y1, x2, y2, ..., x21, y21]
        dla pierwszej wykrytej dłoni.

        Współrzędne są liczone względnie względem nadgarstka (landmark 0).
        Jeśli nie wykryto dłoni, zwraca None.
        """
        if not result.hand_landmarks:
            return None

        hand_landmarks = result.hand_landmarks[0]

        wrist_x = hand_landmarks[0].x
        wrist_y = hand_landmarks[0].y

        row = []

        for lm in hand_landmarks:
            row.append(float(lm.x - wrist_x))
            row.append(float(lm.y - wrist_y))

        return row

    @staticmethod
    def draw_landmarks(frame, result) -> None:
        """
        Rysuje landmarki na klatce do podglądu.
        """
        if not result.hand_landmarks:
            return

        h, w, _ = frame.shape

        for hand_landmarks in result.hand_landmarks:
            for lm in hand_landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)