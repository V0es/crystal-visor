from collections import Counter

import numpy as np
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget

import cv2

from src.ui.widgets.old.last_image import Ui_last_image

class LastImage(QWidget, Ui_last_image):
    image_ready = pyqtSignal()

    def __init__(self, parent=None):
        super(LastImage, self).__init__(parent)

        self.last_image = None
        self.capture = None

        self.setupUi(self)
        self.connect_signals()
        self.init_capture()

    def connect_signals(self):
        self.image_ready.connect(self.display_image)

    def init_capture(self):
        self.capture = cv2.VideoCapture("rtsp://admin:admin@192.168.0.99:554/main")
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        #self.capture.set(cv2.CAP_PROP_FPS, 2)

    def capture_image(self):
        print('image capture')
        if not self.capture.isOpened():
            self.capture.open("rtsp://admin:admin@192.168.0.99:554/main")
        # self.capture.read()
        ret, image = self.capture.read()
        self.last_image = image
        self.capture.release()
        self.image_ready.emit()

    @pyqtSlot()
    def display_image(self):
        print('displaying')
        self.capture.grab()
        image = QImage(
            self.last_image.data,
            self.last_image.shape[1],
            self.last_image.shape[0],
            QImage.Format.Format_RGB888).rgbSwapped()
        self.last_image_label.setPixmap(QPixmap.fromImage(image))

        primitive_dict = self.analyze_image()
        result_dict = self.save_to_csv(primitive_dict, returned=True)
        print('current height: ', list(result_dict.keys())[0] * 10)

    def save_to_csv(self, result_dict, returned=False):
        dict_output = {}

        for length, frequency in result_dict.most_common(5):
            certainty = round(frequency / result_dict.total(), 4)
            if returned:
                dict_output[length] = certainty
        if dict_output:
            return dict_output

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
