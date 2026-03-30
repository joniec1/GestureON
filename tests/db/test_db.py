from db.db_operations import (
    create_user,
    create_session,
    get_gesture_id_by_name,
    insert_sample,
)


def test_create_user():
    user_id = create_user("test_db_user")
    assert user_id is not None
    assert isinstance(user_id, str)
    print("test_create_user PASSED")


def test_get_gesture_id_by_name():
    gesture_id = get_gesture_id_by_name("open_hand")
    assert gesture_id is not None
    assert isinstance(gesture_id, str)
    print("test_get_gesture_id_by_name PASSED")


def test_create_session():
    user_id = create_user("test_session_user")
    gesture_id = get_gesture_id_by_name("open_hand")

    session_id = create_session(
        user_id=user_id,
        gesture_id=gesture_id,
        device_info="pytest_manual",
        lighting="room_light",
    )

    assert session_id is not None
    assert isinstance(session_id, str)
    print("test_create_session PASSED")


def test_insert_sample():
    user_id = create_user("test_sample_user")
    gesture_id = get_gesture_id_by_name("open_hand")
    session_id = create_session(user_id, gesture_id)

    sample_id = insert_sample(
        session_id=session_id,
        frame_index=0,
        landmarks=[0.1, 0.2, 0.3, 0.4],
        is_valid=True,
    )

    assert sample_id is not None
    assert isinstance(sample_id, str)
    print("test_insert_sample PASSED")


if __name__ == "__main__":
    test_create_user()
    test_get_gesture_id_by_name()
    test_create_session()
    test_insert_sample()
    print("ALL DB TESTS PASSED")