"""
Contains method(s) for analyzing images.
"""

from cv2 import cvtColor, COLOR_BGR2GRAY
from numpy import array, average
from PIL.Image import Image


def average_gray_value(img: Image) -> float:
    """
    Calculates average gray value of all pixels of a (color) image.

    For this prupose, the image is first converted to grayscale.

    :param img: (Image) color image
    :return: (float) average gray value
    """
    screen = array(img)
    screen = cvtColor(screen, COLOR_BGR2GRAY)
    return float(average(screen))
