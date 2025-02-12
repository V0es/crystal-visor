import random
import time
import logging

import numpy as np
from PyQt6.QtCore import pyqtSignal

from src.camera.camera_connection_settings import CameraConnection
from src.camera.camera_device import CameraDevice

logger = logging.getLogger(__name__)


class CameraMock(CameraDevice):
    image_ready = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)

    def capture_image(self):
        logger.info('CAPTURING IMAGE')
        image = np.ndarray((1, 1))
        self.image_ready.emit(image)

    def _init_camera(self, connection_params: CameraConnection):
        logger.info('INITIALIZED CAMERA INSTANCE')

    def connect_camera(self, connection_params: CameraConnection):
        self._init_camera(connection_params)
        logger.info('CONNECTING CAMERA')
        logger.info('CAMERA CONNECTED')
        self.opened.emit()

    def get_current_height(self):
        time.sleep(0.5)
        current_height = random.randint(500, 1000) / 100
        logger.info(f'CURRENT HEIGHT CALCULATED: {current_height}')
        self.current_height_ready.emit(current_height)
