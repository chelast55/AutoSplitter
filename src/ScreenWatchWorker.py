from typing import Final

from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Controller as MouseController
from PIL import ImageGrab
import time

from src import SplitsProfile
from src import Config, ImageAnalyzer


class ScreenWatchWorker(QObject):
    _finished: bool = False
    _currently_paused: bool = False
    _mouse = MouseController()
    _keyboard = KeyboardController()
    _blackscreen_counter: int = 0
    _reset_after_this_iteration: bool = False
    _splits_profile: Final[SplitsProfile.SplitsProfile]
    blackscreen_counter_updated: Final[Signal] = Signal(int)
    avg_grey_value_updated: Final[Signal] = Signal(float)

    def __init__(self, _splits_profile):
        super(ScreenWatchWorker, self).__init__()
        self._splits_profile = _splits_profile

    def get_splits_profile(self):
        return self._splits_profile

    def get_blackscreen_counter(self):
        return self._blackscreen_counter

    def is_paused(self):
        return self._currently_paused

    def pause(self):
        print("Worker paused.")
        self._currently_paused = True

    def unpause(self):
        print("Worker unpaused.")
        self._currently_paused = False

    def finish(self):
        self._finished = True

    def run(self):
        def on_key_press(key):
            if repr(key) == repr(Config.decrement_key):
                self._blackscreen_counter -= 1
                print("Blackscreen counter was decremented")
                print("New Blackscreen Count: " + str(self._blackscreen_counter))
                self.blackscreen_counter_updated.emit(self._blackscreen_counter)
                time.sleep(Config.after_key_press_delay)
            elif repr(key) == repr(Config.increment_key):
                self._blackscreen_counter += 1
                print("Blackscreen counter was incremented")
                print("New Blackscreen Count: " + str(self._blackscreen_counter))
                self.blackscreen_counter_updated.emit(self._blackscreen_counter)
                time.sleep(Config.after_key_press_delay)
            elif repr(key) == repr(Config.reset_key):
                self._reset_after_this_iteration = True
                print("Reset!")
                print("Wait for splitter to restart...")
                time.sleep(Config.after_key_press_delay)
            elif repr(key) == repr(Config.pause_key):
                if self._currently_paused:
                    self._currently_paused = False
                    print("Unpaused!")
                else:
                    self._currently_paused = True
                    print("Paused...")
                time.sleep(Config.after_key_press_delay)

        print("Starting splitter worker for profile " + self._splits_profile.name)

        # Enable Keys (Decrement, Increment, Reset, Pause)
        key_press_listener = KeyboardListener(on_press=on_key_press)
        key_press_listener.start()

        # Main loop
        # NOTE: this tool is HEAVILY inspired by this video by Code Bullet: https://www.youtube.com/watch?v=wHRubMACen0
        while not self._finished:
            if not self._currently_paused:
                start_time = time.time()

                # TODO: Only capture the part of the screen which we actually need using bbox="" property.
                # From the Pillow docs:
                # bbox – What region to copy. Default is the entire screen. Note that on Windows OS,
                # the top-left point may be negative if all_screens=True is used.
                img = ImageGrab.grab(all_screens=True)
                img = img.crop(Config.video_preview_coords)

                black_value = ImageAnalyzer.average_gray_value(img)

                self.avg_grey_value_updated.emit(black_value)
                # print("Average Grey Value: " + str(black_value))  # Uncomment this line to output avg grey value

                if black_value <= Config.blackscreen_threshold:
                    self._blackscreen_counter += 1
                    self.blackscreen_counter_updated.emit(self._blackscreen_counter)
                    print("Blackscreen Count: " + str(self._blackscreen_counter))

                    if self._blackscreen_counter in self._splits_profile.splits:
                        print("Pressing " + repr(Config.split_key))
                        self._keyboard.press(Config.split_key)
                    time.sleep(Config.after_split_delay)

                    # print("Time per Cycle: " + str(time.time() - start_time)) # Enable for Debug
                    if (time.time() - start_time) < (1 / Config.max_capture_rate):
                        time.sleep((1 / Config.max_capture_rate) - (time.time() - start_time))

            if self._reset_after_this_iteration:
                self._blackscreen_counter = 0
                self.blackscreen_counter_updated.emit(self._blackscreen_counter)
                self._reset_after_this_iteration = False
                print("Splitter reset!")

    print("Worker stopped.")
