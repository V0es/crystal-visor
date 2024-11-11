import logging
from collections import Counter
from dataclasses import dataclass
from typing import Dict

import cv2
import numpy as np
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QThread, QRunnable

logger = logging.getLogger(__name__)


@dataclass
class AnalysisSettings:
    red_start: int = 105
    red_end: int = 255
    red_speed: int = 10
    blue_start: int = 30
    blue_end: int = 100
    blue_speed: int = 5
    green_start: int = 30
    green_end: int = 100
    green_speed: int = 5
    cut_off: int = 0
    scaling: int = 90
    base_height: float = 25


class WorkerSignals(QObject):
    delta_height_ready = pyqtSignal(float)


class ImageAnalysisWorker(QRunnable):

    def __init__(self, image: np.ndarray, settings: AnalysisSettings = AnalysisSettings()):
        super().__init__()
        self.image = None
        self.signals = WorkerSignals()
        self.settings = settings

    def set_settings(self, new_settings: AnalysisSettings):
        self.settings = new_settings

    @pyqtSlot()
    def run(self):
        if not self.image:
            return
        primitive_dict = self.analyze_image(self.image)
        result_dict = self.save_to_csv(primitive_dict, returned=True)
        current_height = list(result_dict.keys())[0] * 10
        logger.info(f'current height ready: {current_height}')
        self.signals.delta_height_ready.emit(current_height - self.settings.base_height)

    @staticmethod
    def save_to_csv(result_dict, returned=False) -> Dict:
        dict_output = {}

        for length, frequency in result_dict.most_common(5):
            certainty = round(frequency / result_dict.total(), 4)
            if returned:
                dict_output[length] = certainty
        if dict_output:
            return dict_output

    def analyze_image(self, image: np.ndarray) -> Counter:
        logger.info('analyzing image')
        width, height = image.shape[1], image.shape[0]

        upper_red = np.array([0, 0, 255])
        graph = []

        for red in range(self.settings.red_start, self.settings.red_end, self.settings.red_speed):
            lower_red = np.array([0, 0, red])
            for i in range(self.settings.blue_start, self.settings.blue_end + 1, self.settings.blue_speed):
                upper_red[0] = i
                for j in range(self.settings.green_start, self.settings.green_end + 1, self.settings.green_speed):
                    upper_red[1] = j
                    mask = cv2.inRange(image, lower_red, upper_red)

                    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        res = np.vstack(contours)
                    else:
                        continue
                    length = max([k[0][1] for k in res]) - min([k[0][1] for k in res])
                    graph.append(length)

        graph = [round(int(x) / self.settings.scaling, 1)
                 for x in graph if self.settings.cut_off < x < height - self.settings.cut_off]
        result_dict = Counter(graph)

        return result_dict



