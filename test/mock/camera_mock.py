import random
import time

from src.camera.camera_connection_settings import CameraConnection
from src.camera.camera_device import CameraDevice


class CameraMock(CameraDevice):
    def __init__(self, parent=None):
        super().__init__(parent)

    def capture_image(self):
        print('CAPTURING IMAGE')
        self.image_ready.emit()

    def _init_camera(self, connection_params: CameraConnection):
        print('INITIALIZED CAMERA INSTANCE')

    def connect_camera(self, connection_params: CameraConnection):
        self._init_camera(connection_params)
        print('CONNECTING CAMERA')
        print('CAMERA CONNECTED')
        self.opened.emit()

    def get_current_height(self):
        time.sleep(0.5)
        current_height = random.randint(500, 1000) / 100
        print('CURRENT HEIGHT CALCULATED: ', current_height)
        self.current_height_ready.emit(current_height)
