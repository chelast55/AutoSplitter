# NOTE: this tool is HEAVILY inspired by this video from Code Bullet: https://www.youtube.com/watch?v=wHRubMACen0
import numpy as np
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
import cv2
import time

# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
split_key = Key.cmd

# Corners of stream preview window
video_preview_coords = [500, 500, 1780, 1320]

# Blackscreen count values at which to split
splits = [1, 3, 5]

# Threshold for average gray value for a screen to count as blackscreen (0 by default)
blackscreen_threshold = 0

# Times per second a capture is taken (NOTE: this is a maximum)
max_capture_rate = 60

# Delay to prevent multiple splits per blackscreen in seconds
after_split_delay = 10

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    keyboard = Controller()
    blackscreen_counter = 0

    while True:
        start_time = time.time()

        screen = np.array(ImageGrab.grab(bbox=video_preview_coords))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print("Average: " + str(np.average(screen))) # Enable for Debug

        if np.average(screen) <= blackscreen_threshold:
            blackscreen_counter += 1
            print("Blackscreen Count: " + str(blackscreen_counter)) # Enable for Debug
            if blackscreen_counter in splits:
                keyboard.press(split_key)
                keyboard.release(split_key)
            time.sleep(after_split_delay)

        # print("Time per Cycle: " + str(time.time() - start_time)) # Enable for Debug
        while (time.time() - start_time) < (1 / max_capture_rate):
            time.sleep(0.01)

