from typing import List
from PIL import ImageGrab
from PIL.Image import Image
from PySide6.QtCore import QObject, Signal

from src import ImageAnalyzer


class SettingsVideoPreviewWorker(QObject):

    image_captured = Signal(Image)
    gray_value_updated = Signal(float)

    def __init__(self):
        super(SettingsVideoPreviewWorker, self).__init__()
        self._crop_coords = None

    def set_crop_coords(self, crop_coords: List[float]):
        self._crop_coords = crop_coords

    def run(self):
        img: Image = ImageGrab.grab(all_screens=True)
        self.image_captured.emit(img)
        if self._crop_coords is not None:
            cropped_img = img.crop(self._crop_coords)
            self.gray_value_updated.emit(ImageAnalyzer.average_gray_value(cropped_img))
