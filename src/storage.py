from db.landmark_service import LandmarkSessionCollector

class DataStorage:
    def __init__(self, nickname):
        self.nickname = nickname
        self.collector = LandmarkSessionCollector(self.nickname, "init")

    def save(self, data):
        self.collector.save_sample(data)

    def change_gesture(self, new_gesture):
        self.end()
        self.collector = LandmarkSessionCollector(self.nickname, new_gesture)
        self.start()

    def start(self):
        self.collector.start_session()

    def end(self):
        self.collector.end_session()


