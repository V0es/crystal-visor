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

        center = image.shape[1] // 2
        height = image.shape[0]

        image = image[
                self.settings.cut_off:height - self.settings.cut_off,
                center - self.settings.width_gap:center + self.settings.width_gap
                ]

        mask = cv2.inRange(image, self.settings.lower_red_bgr, self.settings.upper_red_bgr)
        heights = []

        for _ in range(self.settings.search_iterations):
            # Поиск контуров
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                two_largest_contours = heapq.nlargest(2, contours, key=cv2.contourArea)

                for contour in two_largest_contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.drawContours(image, two_largest_contours, -1, (0, 255, 0), 3)

                if len(two_largest_contours) < 2:
                    logger.error('could not find 2 contours')
                    return self.settings.base_height

                upper_contour, bottom_contour = two_largest_contours
                upper_y_coords = upper_contour[:, 0, 1]
                upper_top_point = upper_contour[np.argmin(upper_y_coords)]

                bottom_y_coords = bottom_contour[:, 0, 1]
                bottom_low_point = bottom_contour[np.argmax(bottom_y_coords)]

                height = abs(upper_top_point[0][1] - bottom_low_point[0][1])
                heights.append(height)

            else:
                print('Контуры не найдены.')
                return 0

        try:
            self.save_image(image)
        except Exception as e:
            logger.error(f'unable to save image: {e}')
        heights_counter = Counter(heights)

        most_common_height, _ = heights_counter.most_common(1)[0]

        height_in_millimeters = most_common_height / self.settings.scaling
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
        formatted_time = time.strftime("%H-%M-%S_%d-%m-%Y")
        cv2.imwrite(f'./logs/analysis/imgs/{formatted_time}.png', image)




