# NOTE: this tool is HEAVILY inspired by this video from Code Bullet: https://www.youtube.com/watch?v=wHRubMACen0
import numpy as np
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from PIL import ImageGrab
import cv2
import time

# Do setup at start?
setup_at_start = True  # TODO: impement that user inpus are saved in and loaded from config file

# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
split_key = Key.cmd

# Corners of stream preview window
video_preview_coords = [0, 0, 100, 100]

# Blackscreen count values at which to split # TODO: move to splits.txt
splits = [1, 3, 5]

# Threshold for average gray value for a screen to count as blackscreen (0 by default) # TODO: move to config.txt
blackscreen_threshold = 0

# Times per second a capture is taken (NOTE: this is a maximum and possibly unreachable) # TODO: move to config.txt
max_capture_rate = 60

# Delay to prevent multiple splits per blackscreen in seconds # TODO: move to config.txt
after_split_delay = 10


if __name__ == '__main__':
    mouse = MouseController()
    keyboard = KeyboardController()
    preview_coord_counter = 0
    blackscreen_counter = 0

    def correct_coords():
        global video_preview_coords
        # check x coords
        if video_preview_coords[2] < video_preview_coords[0]:
            # swap x1 and x2
            temp = video_preview_coords[0]
            video_preview_coords[0] = video_preview_coords[2]
            video_preview_coords[2] = temp
        elif video_preview_coords[2] == video_preview_coords[0]:
            video_preview_coords[2] += 1

        # check y coords
        if video_preview_coords[3] < video_preview_coords[1]:
            # swap y1 and y2
            temp = video_preview_coords[1]
            video_preview_coords[1] = video_preview_coords[3]
            video_preview_coords[3] = temp
        elif video_preview_coords[3] == video_preview_coords[1]:
            video_preview_coords[3] += 1

    def on_click_set_coords(x, y, button, pressed):
        global video_preview_coords
        global preview_coord_counter
        if button == Button.left and pressed:
            if preview_coord_counter == 0:
                video_preview_coords[0] = x
                video_preview_coords[1] = y
                preview_coord_counter += 1
                print("First Corner set to (" + str(x) + "," + str(y) + ")")
            else:
                video_preview_coords[2] = x
                video_preview_coords[3] = y
                preview_coord_counter += 1
                print("Second Corner set to (" + str(x) + "," + str(y) + ")")
                correct_coords()
                return False

    # Setup
    if setup_at_start:
        # Set Split Key
        print("Press Split Key")
        # TODO: implement

        # Set video preview coords
        print("Click to set video preview coords (pick 2 diagonally opposed corners)")
        with MouseListener(on_click=on_click_set_coords) as mouse_listener:
            mouse_listener.join()

        # Enable/Disable setup on future program starts depending on user input
        print("Setup done!")
        print("Don't forget to enter your splits manually in splits.txt!")
        input("Skip setup at future program starts? (y/n)")
        # TODO: implement

    while True:
        start_time = time.time()

        screen = np.array(ImageGrab.grab(bbox=video_preview_coords))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # print("Average Grey Value: " + str(np.average(screen))) # Enable for Debug

        if np.average(screen) <= blackscreen_threshold:
            blackscreen_counter += 1
            print("Blackscreen Count: " + str(blackscreen_counter))
            if blackscreen_counter in splits:
                keyboard.press(split_key)
                keyboard.release(split_key)
            time.sleep(after_split_delay)

        # print("Time per Cycle: " + str(time.time() - start_time)) # Enable for Debug
        while (time.time() - start_time) < (1 / max_capture_rate):
            time.sleep(0.01)

