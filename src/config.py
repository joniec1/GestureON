from pathlib import Path
from enum import Enum

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

HAND_LANDMARKER_PATH = PROJECT_ROOT / "model" / "hand_landmarker.task"
MODEL_PATH = PROJECT_ROOT / "model" / "model.pkl"
DATA_DIR = PROJECT_ROOT / "data"


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


