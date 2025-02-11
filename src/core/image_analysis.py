import heapq
import logging
from collections import Counter
from dataclasses import dataclass, field
from types import NoneType
import datetime
from typing import Dict

import cv2
import numpy as np
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QThread, QRunnable

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f'./logs/analysis/img_anlsys.log', mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@dataclass
class AnalysisSettings:
    lower_red_bgr: np.ndarray = field(default_factory=lambda: np.array([33, 39, 79]))
    upper_red_bgr: np.ndarray = field(default_factory=lambda: np.array([60, 60, 255]))

    search_iterations: int = 1

    cut_off: int = 50
    scaling: int = 11.57
    base_height: float = 25
    height_gap: float = 5
    width_gap: int = 200


class WorkerSignals(QObject):
    delta_height_ready = pyqtSignal(float)


class ImageAnalysisWorker(QRunnable):

    def __init__(self, image: np.ndarray, settings: AnalysisSettings = AnalysisSettings()):
        super().__init__()
        self.image = image
        self.signals = WorkerSignals()
        self.settings = settings

    def set_settings(self, new_settings: AnalysisSettings):
        self.settings = new_settings

    @pyqtSlot()
    def run(self):
        if isinstance(self.image, NoneType):
            return
        current_height = round(self.analyze_image(self.image), 3)
        logger.info(f'current height ready: {current_height}')
        delta_height = current_height - self.settings.base_height
        if -self.settings.height_gap <= delta_height <= self.settings.height_gap:
            logger.info('delta height is in 5mm gap, no temp adjustment needed')
            return
        self.signals.delta_height_ready.emit(delta_height)


    def analyze_image(self, image: np.ndarray) -> float:
        logger.info('analyzing image')

        cut_off = 20
        wight_gap = 200
        scaling = 13.

        low_hsv = (0, 160, 111)
        high_hsv = (10, 255, 255)

        center = image.shape[1] // 2
        height = image.shape[0]
        image = image[cut_off:height - cut_off, center - wight_gap:center + wight_gap]

        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, low_hsv, high_hsv)

        for _ in range(1):
            # Поиск контуров
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)

                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3)

                contour_y_coords = largest_contour[:, 0, 1]
                contour_top_point = largest_contour[np.argmin(contour_y_coords)]

                height = image.shape[0] - contour_top_point[0][1]

            else:
                print('Контуры не найдены.')
                height = 0
        try:
            self.save_image(image)
        except Exception as e:
            logger.error(f'unable to save image: {e}')
        height_in_millimeters = height / self.settings.scaling
        return height_in_millimeters

    @staticmethod
    def save_image(image: np.ndarray):
        """
        Function is part of logging system
        Saves image with timestamp in filename
        :param image: Image to save
        :return: None
        """
        time = datetime.datetime.now()
        formatted_time = time.strftime("%d-%m-%Y_%H-%M-%S")
        cv2.imwrite(f'./logs/analysis/imgs/{formatted_time}.png', image)




