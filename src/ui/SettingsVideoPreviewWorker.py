from typing import Optional
from PIL import ImageGrab
from PIL.Image import Image
from PySide6.QtCore import QObject, Signal

from src.image_analyzer import average_gray_value


class SettingsVideoPreviewWorker(QObject):

    image_captured: Signal = Signal(Image)
    gray_value_updated: Signal = Signal(float)

    def __init__(self):
        super(SettingsVideoPreviewWorker, self).__init__()
        self._crop_coords: Optional[tuple[float, float, float, float]] = None

    def set_crop_coords(self, crop_coords: tuple[float, float, float, float]):
        self._crop_coords = crop_coords

    def run(self):
        img: Image = ImageGrab.grab(all_screens=True)
        self.image_captured.emit(img)
        if self._crop_coords is not None:
            cropped_img = img.crop(self._crop_coords)
            self.gray_value_updated.emit(average_gray_value(cropped_img))
