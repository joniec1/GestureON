import sys
import os
from pathlib import Path
from enum import Enum

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path

    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / relative_path

MODEL_DIR = get_resource_path("model")
DATA_DIR = get_resource_path("data")

HAND_LANDMARKER_PATH = MODEL_DIR / "hand_landmarker.task"
MODEL_PATH = MODEL_DIR / "model.pkl"


class GestureLabel(Enum):
    NO_HAND = -1
    OPEN_HAND = 0
    FIST = 1
    THUMB_UP = 2

GESTURE_TEXT = {
    GestureLabel.NO_HAND: "No hand",
    GestureLabel.OPEN_HAND: "Open hand",
    GestureLabel.FIST: "Fist",
    GestureLabel.THUMB_UP: "Thumbs up"
}


