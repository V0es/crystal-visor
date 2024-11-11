import logging
import random
import time

from src.core.image_analysis import ImageAnalysisWorker


logger = logging.getLogger(__name__)


class ImageAnalysisMock(ImageAnalysisWorker):
    def __init__(self, image):
        super().__init__(image)

    def run(self):
        logger.info(f'CALCULATING DELTA HEIGHT')
        current_height = random.randint(25, 45)
        time.sleep(4)
        delta_height = current_height - self.settings.base_height
        logger.info(f'CALCULATED DELTA HEIGHT: {delta_height}')
        self.signals.delta_height_ready.emit(delta_height)

