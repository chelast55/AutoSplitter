from PySide6 import QtCore
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
import numpy as np
from PIL import ImageGrab
import cv2
import time
import SplitsProfile
import Config


class ScreenWatchWorker(QtCore.QObject):
    _finished: bool = False
    currently_paused: bool = False
    mouse = MouseController()
    keyboard = KeyboardController()
    blackscreen_counter: int = 0
    reset_after_this_iteration: bool = False
    _splits_profile: SplitsProfile.SplitsProfile = None

    def __init__(self, _splits_profile):
        super(ScreenWatchWorker, self).__init__()
        self._splits_profile = _splits_profile

    @property
    def splits_profile(self):
        return self._splits_profile

    def finish(self):
        self._finished = True

    def run(self):
        def on_key_press(key):
            if repr(key) == Config.decrement_key:
                self.blackscreen_counter -= 1
                print("Blackscreen counter was decremented")
                print("New Blackscreen Count: " + str(self.blackscreen_counter))
                time.sleep(Config.after_key_press_delay)
            elif repr(key) == Config.increment_key:
                self.blackscreen_counter += 1
                print("Blackscreen counter was incremented")
                print("New Blackscreen Count: " + str(self.blackscreen_counter))
                time.sleep(Config.after_key_press_delay)
            elif repr(key) == Config.reset_key:
                self.reset_after_this_iteration = True
                print("Reset!")
                print("Wait for splitter to restart...")
                time.sleep(Config.after_key_press_delay)
            elif repr(key) == Config.pause_key:
                if self.currently_paused:
                    self.currently_paused = False
                    print("Unpaused!")
                else:
                    self.currently_paused = True
                    print("Paused...")
                time.sleep(Config.after_key_press_delay)

        print("Starting splitter worker for profile " + self.splits_profile.name)

        # Enable Keys (Decrement, Increment, Reset, Pause)
        key_press_listener = KeyboardListener(on_press=on_key_press)
        key_press_listener.start()

        # Main loop
        # NOTE: this tool is HEAVILY inspired by this video by Code Bullet: https://www.youtube.com/watch?v=wHRubMACen0
        while not self._finished:
            if not self.currently_paused:
                start_time = time.time()

                screen = np.array(ImageGrab.grab(bbox=Config.video_preview_coords))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                print("Average Grey Value: " + str(np.average(screen)))  # Enable for Debug

                if np.average(screen) <= Config.blackscreen_threshold:
                    self.blackscreen_counter += 1
                    print("Blackscreen Count: " + str(self.blackscreen_counter))
                    if self.blackscreen_counter in self._splits_profile.splits:
                        print("Pressing " + repr(Config.split_key))
                        self.keyboard.press(Config.split_key)
                    time.sleep(Config.after_split_delay)

                    # print("Time per Cycle: " + str(time.time() - start_time)) # Enable for Debug
                    if (time.time() - start_time) < (1 / Config.max_capture_rate):
                        time.sleep((1 / Config.max_capture_rate) - (time.time() - start_time))

            if self.reset_after_this_iteration:
                self.blackscreen_counter = 0
                self.reset_after_this_iteration = False
                print("Splitter reset!")
