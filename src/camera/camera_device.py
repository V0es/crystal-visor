from collections import Counter

import cv2
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from .camera_connection_settings import CameraConnection


class CameraDevice(QObject):
    opened = pyqtSignal()
    image_ready = pyqtSignal()
    current_height_ready = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.connection_settings = None
        self.capture = None
        self.last_image = None

    def connect_signals(self):
        self.image_ready.connect(self.get_current_height)

    def capture_image(self):
        if not self.capture:
            return

        if not self.capture.isOpened():
            # TODO: move address to config
            self.capture.open("rtsp://admin:admin@192.168.0.99:554/main")
        ret, image = self.capture.read()
        self.last_image = image
        self.capture.release()
        self.image_ready.emit()

    def _init_camera(self, connection_params: CameraConnection):
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
            self.capture.open()
            self.opened.emit()
        except Exception as e:
            print('unlucky')

    # !!TEMPORARY!! TODO: move to separate module
    @staticmethod
    def save_to_csv(result_dict, returned=False):
        dict_output = {}

        for length, frequency in result_dict.most_common(5):
            certainty = round(frequency / result_dict.total(), 4)
            if returned:
                dict_output[length] = certainty
        if dict_output:
            return dict_output

    @pyqtSlot()
    def get_current_height(self):
        primitive_dict = self.analyze_image()
        result_dict = self.save_to_csv(primitive_dict, returned=True)
        current_height = list(result_dict.keys())[0] * 10
        print('current height ready', current_height)
        self.current_height_ready.emit(current_height)

    def analyze_image(self):
        print('Analyzing...')
        im = self.last_image
        width, height = im.shape[1], im.shape[0]

        upper_red = np.array([0, 0, 255])
        graph = []

        RED_START = 105
        RED_END = 255
        RED_SPEED = 10
        BLUE_START = 30
        BLUE_END = 100
        BLUE_SPEED = 5
        GREEN_START = 30
        GREEN_END = 100
        GREEN_SPEED = 5
        CUT_OFF = 10
        SCALING = 135

        for red in range(RED_START, RED_END, RED_SPEED):
            lower_red = np.array([0, 0, red])
            for i in range(BLUE_START, BLUE_END + 1, BLUE_SPEED):
                upper_red[0] = i
                for j in range(GREEN_START, GREEN_END + 1, GREEN_SPEED):
                    upper_red[1] = j
                    mask = cv2.inRange(im, lower_red, upper_red)

                    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        res = np.vstack(contours)
                    else:
                        continue
                    length = max([k[0][1] for k in res]) - min([k[0][1] for k in res])
                    graph.append(length)

        graph = [round(int(x) / SCALING, 1) for x in graph if CUT_OFF < x < height - CUT_OFF]
        result_dict = Counter(graph)

        # Save histogram to file

        return result_dict
