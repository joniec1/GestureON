from db.landmark_service import LandmarkSessionCollector


def test_start_session():
    collector = LandmarkSessionCollector(
        nickname="test_landmark_user",
        gesture_name="open_hand",
        device_info="pytest_manual",
        lighting="room_light",
    )

    session_id = collector.start_session()

    assert session_id is not None
    assert collector.is_session_active is True
    assert collector.session_id is not None
    assert collector.user_id is not None
    assert collector.gesture_id is not None
    assert collector.frame_counter == 0

    print("test_start_session PASSED")


def test_save_sample():
    collector = LandmarkSessionCollector(
        nickname="test_landmark_sample_user",
        gesture_name="open_hand",
    )

    collector.start_session()

    sample_id = collector.save_sample([0.1, 0.2, 0.3, 0.4])

    assert sample_id is not None
    assert collector.frame_counter == 1

    print("test_save_sample PASSED")


def test_end_session():
    collector = LandmarkSessionCollector(
        nickname="test_landmark_end_user",
        gesture_name="open_hand",
    )

    collector.start_session()
    collector.end_session()

    assert collector.is_session_active is False

    print("test_end_session PASSED")


def test_save_sample_without_session():
    collector = LandmarkSessionCollector(
        nickname="test_no_session",
        gesture_name="open_hand",
    )

    try:
        collector.save_sample([0.1, 0.2, 0.3])
        raise AssertionError("Expected RuntimeError was not raised")
    except RuntimeError:
        print("test_save_sample_without_session PASSED")


if __name__ == "__main__":
    test_start_session()
    test_save_sample()
    test_end_session()
    test_save_sample_without_session()
    print("ALL LANDMARK SERVICE TESTS PASSED")