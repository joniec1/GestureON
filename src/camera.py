from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import mediapipe as mp
import time

from mediapipe.tasks.python import vision, BaseOptions

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(object) # frame
    data_signal = pyqtSignal(object) # data for AI

    def __init__(self, url, model):
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

            self.data_signal.emit(result)

            if result.hand_landmarks:
                h, w, _ = frame.shape
                for hand_landmarks in result.hand_landmarks:
                    for lm in hand_landmarks:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)


            self.change_pixmap_signal.emit(frame)

        cap.release()
    
    def stop(self):
        self._running = False
