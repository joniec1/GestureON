from __future__ import annotations

from typing import Any, Sequence


from db.db_operations import (
    create_user,
    create_session,
    get_gesture_id_by_name,
    insert_sample,
)


class LandmarkSessionCollector:
    """
    Klasa obsługująca pełny flow:
    user -> session -> samples

    Użycie:
        collector = LandmarkSessionCollector(
            nickname="janek",
            gesture_name="open_hand",
            device_info="mobile_app",
            lighting="room_light"
        )

        collector.start_session()
        collector.save_sample([0.1, 0.2, 0.3, 0.4, ...])
        collector.end_session()
    """

    def __init__(
        self,
        nickname: str,
        gesture_name: str,
        device_info: str | None = None,
        lighting: str | None = None,
        validate_landmarks: bool = True,
        auto_create_user: bool = True,
    ) -> None:
        self.nickname = nickname
        self.gesture_name = gesture_name
        self.device_info = device_info
        self.lighting = lighting

        self.validate_landmarks = validate_landmarks
        self.auto_create_user = auto_create_user

        self.user_id: str | None = None
        self.gesture_id: str | None = None
        self.session_id: str | None = None

        self.frame_counter: int = 0
        self.is_session_active: bool = False

    # =========================
    # Public API
    # =========================

    def start_session(self) -> str:
        """
        Przygotowuje usera, pobiera gesture_id i tworzy nową sesję.

        Returns:
            str: session_id
        """
        if self.is_session_active:
            raise RuntimeError("Session is already active.")

        self._ensure_user()
        self._load_gesture()
        self._create_session()

        self.frame_counter = 0
        self.is_session_active = True

        return self.session_id  # type: ignore[return-value]

    def save_sample(self, landmarks: Sequence[float | int]) -> str:
        """
        Zapisuje pojedynczą próbkę (np. jedną klatkę landmarków) do bazy.

        Args:
            landmarks: lista / sekwencja wartości landmarków

        Returns:
            str: sample_id
        """
        if not self.is_session_active or self.session_id is None:
            raise RuntimeError("Session is not active. Call start_session() first.")

        landmarks_list = self._prepare_landmarks(landmarks)

        if self.validate_landmarks:
            self._validate_landmarks(landmarks_list)

        sample_id = self._insert_sample(
            frame_index=self.frame_counter,
            landmarks=landmarks_list,
        )

        self.frame_counter += 1
        return sample_id

    def end_session(self) -> None:
        """
        Kończy sesję logicznie.
        Na ten moment nie zapisuje dodatkowych danych do DB.
        """
        if not self.is_session_active:
            return

        self.is_session_active = False

    def reset_session(self) -> None:
        """
        Czyści stan sesji.
        """
        self.session_id = None
        self.frame_counter = 0
        self.is_session_active = False

    def get_status(self) -> dict[str, Any]:
        """
        Zwraca aktualny stan obiektu.
        """
        return {
            "nickname": self.nickname,
            "gesture_name": self.gesture_name,
            "user_id": self.user_id,
            "gesture_id": self.gesture_id,
            "session_id": self.session_id,
            "frame_counter": self.frame_counter,
            "is_session_active": self.is_session_active,
        }

    # =========================
    # Private methods
    # =========================

    def _ensure_user(self) -> None:
        """
        Tworzy usera, jeśli potrzeba.
        Na ten moment zawsze tworzy nowego usera.
        """
        if self.user_id is not None:
            return

        if not self.auto_create_user:
            raise RuntimeError("User does not exist and auto_create_user is disabled.")

        self.user_id = create_user(self.nickname)

    def _load_gesture(self) -> None:
        """
        Pobiera gesture_id na podstawie gesture_name.
        """
        if self.gesture_id is not None:
            return

        self.gesture_id = get_gesture_id_by_name(self.gesture_name)

    def _create_session(self) -> None:
        """
        Tworzy rekord sesji w bazie.
        """
        if self.user_id is None:
            raise RuntimeError("user_id is missing.")
        if self.gesture_id is None:
            raise RuntimeError("gesture_id is missing.")

        self.session_id = create_session(
            user_id=self.user_id,
            gesture_id=self.gesture_id,
            device_info=self.device_info,
            lighting=self.lighting,
        )

    def _insert_sample(self, frame_index: int, landmarks: list[float]) -> str:
        """
        Zapis próbki do bazy.
        """
        if self.session_id is None:
            raise RuntimeError("session_id is missing.")

        return insert_sample(
            session_id=self.session_id,
            frame_index=frame_index,
            landmarks=landmarks,
            is_valid=True,
        )

    def _validate_landmarks(self, landmarks: list[float]) -> None:
        """
        Podstawowa walidacja danych wejściowych.
        Na razie:
        - musi być lista liczb
        - nie może być pusta

        Później można dodać:
        - długość == 42
        - brak NaN
        - zakresy wartości
        """
        if not isinstance(landmarks, list):
            raise TypeError("Landmarks must be a list.")

        if len(landmarks) == 0:
            raise ValueError("Landmarks list is empty.")

        for value in landmarks:
            if not isinstance(value, (int, float)):
                raise TypeError("All landmark values must be int or float.")

    def _prepare_landmarks(self, landmarks: Sequence[float | int]) -> list[float]:
        """
        Zamienia wejście na zwykłą listę floatów.
        """
        return [float(x) for x in landmarks]