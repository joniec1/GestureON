from supabase_client import supabase


def get_gesture_id_by_name(gesture_name: str):
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


def create_user(nickname: str):
    response = (
        supabase.table("users")
        .insert({"nickname": nickname})
        .execute()
    )
    return response.data[0]["id"]


def create_session(user_id: str, gesture_id: str, device_info=None, lighting=None):
    payload = {
        "user_id": user_id,
        "gesture_id": gesture_id,
        "device_info": device_info,
        "lighting": lighting,
    }

    response = supabase.table("sessions").insert(payload).execute()
    return response.data[0]["id"]


def insert_sample(session_id: str, frame_index: int, landmarks: list, is_valid=True):
    payload = {
        "session_id": session_id,
        "frame_index": frame_index,
        "landmarks": landmarks,
        "is_valid": is_valid,
    }

    response = supabase.table("samples").insert(payload).execute()
    return response.data[0]["id"]