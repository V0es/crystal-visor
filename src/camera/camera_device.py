from collections import Counter
import logging

import cv2
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from .camera_connection_settings import CameraConnection

logger = logging.getLogger(__name__)


class CameraDevice(QObject):
    opened = pyqtSignal()
    image_ready = pyqtSignal(np.ndarray)

    connection_lost = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.connection_params: CameraConnection | None = None
        self.capture = None
        self.last_image = None

        self.connect_signals()

    def connect_signals(self):
        pass

    @pyqtSlot()
    def capture_image(self):
        logger.info('capturing image')
        if not self.capture:
            logger.warning('no capture object')
            return

        ret, image = self.capture.read()
        self.last_image = image
        self.capture.release()
        self.image_ready.emit(image)

    def _init_camera(self, connection_params: CameraConnection):
        logger.info('initializing capture')
        self.connection_params = connection_params
        self.capture = cv2.VideoCapture(
            f'rtsp://{connection_params.username}:'
            f'{connection_params.password}@'
            f'{connection_params.ip_address}:'
            f'{connection_params.port}/'
            f'{connection_params.stream}'
        )
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def connect_camera(self, connection_params: CameraConnection):
        self._init_camera(connection_params)
        try:
            logger.info('trying to connect camera')
            self.capture.open(
                f'rtsp://{connection_params.username}:'
                f'{connection_params.password}@'
                f'{connection_params.ip_address}:'
                f'{connection_params.port}/'
                f'{connection_params.stream}'
            )
            self.opened.emit()
        except cv2.error as error:
            self.connection_lost.emit()
            logger.error(f'unable to connect camera: {error}')

