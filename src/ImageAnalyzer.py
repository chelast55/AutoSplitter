"""
Contains method(s) for analyzing images.
"""

import cv2
import numpy as np
from PIL.Image import Image


def average_gray_value(img: Image) -> float:
    """
    Calculates average gray value of all pixels of a (color) image.

    For this prupose, the image is first converted to grayscale.

    :param img: (Image) color image
    :return: (double) average gray value
    """
    screen = np.array(img)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    return np.average(screen)
