import random

import numpy as np

from src.core.image_analysis import ImageAnalysisThread


class ImageAnalysisMock(ImageAnalysisThread):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        current_height = random.randint(25, 45)
        self.delta_height_ready.emit(current_height - self.settings.base_height)

