from config import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QInputDialog, QStackedWidget
from PyQt5.QtGui import QImage, QPixmap
from camera import CameraThread
from model import ModelAI



class Mode:
    COLLECT = 0
    RECOGNIZE = 1

class MainWindow(QMainWindow):
    def __init__(self, source, mode):
        super().__init__()
        self.display_label = QLabel(self)
        self.setup_ui()
        self.setup_overlay()
        
        self.saving = False
        self.label = None

        self.mode = mode
        self.change_label_mode()

        self.model = ModelAI()
        self.model_functions = {
            Mode.COLLECT: self.model.collect,
            Mode.RECOGNIZE: self.model.recognize
        }

        self.camera_thread = CameraThread(source, str(HAND_LANDMARKER_PATH))
        self.setup_signal()


    def setup_signal(self):
        self.camera_thread.change_pixmap_signal.connect(self.update_cam)
        self.camera_thread.data_signal.connect(self.process_data)
        self.camera_thread.start()


    def setup_ui(self):
        self.setWindowTitle("GestureON")
        self.setGeometry(900, 500, 500, 500)
        self.display_label.setMinimumSize(10,10)
        self.setCentralWidget(self.display_label)
        self.setMinimumSize(300,300)

    def setup_overlay(self):
        self.text_label = QLabel(self.display_label)
        self.text_label.setStyleSheet("""
            color: green;
            font-size: 18px;
            background: rgba(0,0,0,120);
            padding: 5px;
        """)
        self.text_label.move(10, 10)
        self.text_label.setText("")
        self.text_label.raise_()


    def process_data(self, data):
        handler = self.model_functions.get(self.mode)

        if not handler:
            return
        
        if self.mode == Mode.COLLECT and self.saving:
            label_text = handler(data, self.label)
            self.saving = False
            self.draw_label(label_text)

        elif self.mode == Mode.RECOGNIZE:
            label_text = handler(data)
            self.draw_label(label_text)


    def update_cam(self, cv_img):
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.display_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )
        self.display_label.setPixmap(scaled_pixmap)

    def closeEvent(self, event): # type: ignore
        self.camera_thread.stop()
        self.camera_thread.wait()
        
        event.accept()

    def keyPressEvent(self, event): # type: ignore
        if event.key() == Qt.Key.Key_C:
            self.change_label_mode()
        elif event.key() == Qt.Key.Key_S:
            self.saving = True
        elif event.key() == Qt.Key.Key_Q:
            self.close()

    def change_label_mode(self):
        if self.mode == Mode.COLLECT:
            label, ok = QInputDialog.getText(self, "Label", "Podaj numer znaku:")
            if ok:
                self.label = int(label)
                self.draw_label(GESTURE_TEXT[GestureLabel(self.label)])

    def draw_label(self, text):
        self.text_label.setText(text)
        self.text_label.adjustSize()



class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
         
        self.source = None
        self.mode = None
        self.stack = QStackedWidget()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.stack)

        self.init_camera_page()
        self.init_mode_page()



    def init_camera_page(self):
        self.camera_page = QWidget()
        layout = QVBoxLayout()

        self.btn_local_0 = QPushButton("Camera 0")
        self.btn_local_1 = QPushButton("Camera 1")
        self.btn_ip = QPushButton("IP Camera")

        self.btn_local_0.clicked.connect(lambda : self.start_local(0))
        self.btn_local_1.clicked.connect(lambda : self.start_local(1))
        self.btn_ip.clicked.connect(self.start_ip)

        layout.addWidget(self.btn_local_0)
        layout.addWidget(self.btn_local_1)
        layout.addWidget(self.btn_ip)

        self.camera_page.setLayout(layout)
        self.stack.addWidget(self.camera_page)

    def init_mode_page(self):
        self.mode_page = QWidget()
        layout = QVBoxLayout()

        self.btn_collect = QPushButton("Collect")
        self.btn_test = QPushButton("Test")

        self.btn_collect.clicked.connect(lambda : self.set_mode(Mode.COLLECT))
        self.btn_test.clicked.connect(lambda : self.set_mode(Mode.RECOGNIZE))

        layout.addWidget(self.btn_collect)
        layout.addWidget(self.btn_test)

        self.mode_page.setLayout(layout)
        self.stack.addWidget(self.mode_page)

    def start_local(self, index):
        self.source = index
        self.stack.setCurrentWidget(self.mode_page)

    def start_ip(self):
        url, ok = QInputDialog.getText(self, "IP Camera", "Podaj URL:")
        if ok:
            self.source = url
            self.stack.setCurrentWidget(self.mode_page)

    def set_mode(self, new_mode):
        self.mode = new_mode
        self.open_main()


    def open_main(self):
        self.main = MainWindow(self.source, self.mode)
        self.main.show()
        self.close()
