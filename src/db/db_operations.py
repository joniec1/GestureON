"""
Low-level operacje na bazie danych (Supabase).

Zawiera proste funkcje CRUD używane przez wyższe warstwy (np. landmark_service).
Każda funkcja wykonuje pojedyncze zapytanie do bazy.
"""

from db.supabase_client import supabase


def get_gesture_id_by_name(gesture_name: str) -> str:
    """
    Zwraca ID gestu na podstawie jego nazwy.
    """
    response = (
        supabase.table("gestures")
        .select("id")
        .eq("name", gesture_name)
        .execute()
    )

    data = response.data
    if not data:
        raise ValueError(f"Gesture '{gesture_name}' not found in database.")

    return data[0]["id"]


def create_user(nickname: str) -> str:
    """
    Tworzy użytkownika i zwraca jego ID.
    """
    response = (
        supabase.table("users")
        .insert({"nickname": nickname})
        .execute()
    )

    if not response.data:
        raise RuntimeError("Failed to create user.")

    return response.data[0]["id"]


def create_session(
    user_id: str,
    gesture_id: str,
    device_info: str | None = None,
    lighting: str | None = None,
) -> str:
    """
    Tworzy sesję i zwraca jej ID.
    """
    payload = {
        "user_id": user_id,
        "gesture_id": gesture_id,
        "device_info": device_info,
        "lighting": lighting,
    }

    response = supabase.table("sessions").insert(payload).execute()

    if not response.data:
        raise RuntimeError("Failed to create session.")

    return response.data[0]["id"]


def insert_sample(
    session_id: str,
    frame_index: int,
    landmarks: list,
    is_valid: bool = True,
) -> str:
    """
    Zapisuje próbkę (landmarki) i zwraca jej ID.
    """
    payload = {
        "session_id": session_id,
        "frame_index": frame_index,
        "landmarks": landmarks,
        "is_valid": is_valid,
    }

    response = supabase.table("samples").insert(payload).execute()

    if not response.data:
        raise RuntimeError("Failed to insert sample.")

    return response.data[0]["id"]