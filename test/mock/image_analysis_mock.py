import random

import numpy as np

from src.core.image_analysis import ImageAnalysis


class ImageAnalysisMock(ImageAnalysis):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def get_delta_height(self, image: np.ndarray) -> None:
        current_height = random.randint(25, 45)
        self.delta_height_ready.emit(current_height - self.settings.base_height)

