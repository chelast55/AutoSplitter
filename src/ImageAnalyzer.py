import cv2
import numpy as np
from PIL.Image import Image


def average_gray_value(img: Image):
    screen = np.array(img)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    return np.average(screen)
