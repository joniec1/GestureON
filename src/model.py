import joblib
import csv
from config import MODEL_PATH, GESTURE_TEXT, DATA_DIR, GestureLabel
import numpy as np


labels = ["open_hand", "fist", "thumbs_up"] # test
class ModelAI:
    def __init__(self):
        self.model = joblib.load(str(MODEL_PATH))

    def recognize(self, result):
        data = []
        pred = -1
        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                for lm in hand_landmarks:
                    data.append(lm.x)
                    data.append(lm.y)

                if len(data) == 42:
                    X = np.array(data).reshape(1, -1)
                    pred = self.model.predict(X)[0]
                    
        return GESTURE_TEXT[GestureLabel(pred)]

    def collect(self, result, label):

        data = []
        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                for lm in hand_landmarks:
                    data.append(lm.x)
                    data.append(lm.y)

        return GESTURE_TEXT[GestureLabel(label)], data



        
