import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal


class CameraStream(QThread):
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_running = False

    def run(self):
        pass
