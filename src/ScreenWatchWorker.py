"""
Contains ScreenWatchWorker class
"""

from typing import Final, Optional
from PySide6.QtCore import QObject, Signal
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Controller as MouseController
from time import time, sleep
from dxcam import create as dxcam_create, DXCamera
from numpy import ndarray

from src import config
from src.image_analyzer import average_gray_value
from src.SplitsProfile import SplitsProfile

DEBUG_PRINTS: bool = False


class ScreenWatchWorker(QObject):
    """
    TODO: further improve this

    :param _splits_profile: (SplitsProfile) splits profile to save internally
    """
    blackscreen_counter_updated: Final[Signal] = Signal(int)
    """Signal that emits blackscreen count whenever it changes"""
    avg_grey_value_updated: Final[Signal] = Signal(float)
    """Signal that emits average gray value whenever it is re-calculated"""
    pause_status_updated: Final[Signal] = Signal()
    """Signal that emits current pause status whenever it changes"""
    _finished: bool = False
    _currently_paused: bool = False
    _mouse: MouseController = MouseController()
    _keyboard: KeyboardController = KeyboardController()
    _blackscreen_counter: int = 0
    _reset_after_this_iteration: bool = False
    _splits_profile: Final[SplitsProfile]
    _key_press_listener: Final[KeyboardListener]

    def __init__(self, _splits_profile: SplitsProfile):
        super(ScreenWatchWorker, self).__init__()
        self._splits_profile: SplitsProfile = _splits_profile
        self._key_press_listener: KeyboardListener = KeyboardListener(on_press=self.on_key_press)
        self._averaged_per_cycle_time: Optional[float] = None
        self._camera: DXCamera = dxcam_create()

    # region getters
    def get_splits_profile(self) -> SplitsProfile:
        return self._splits_profile

    def get_blackscreen_counter(self) -> int:
        return self._blackscreen_counter

    def is_paused(self) -> bool:
        return self._currently_paused

    def get_per_cycle_time(self) -> float:  # s
        if self._averaged_per_cycle_time is None:
            return 999.999
        return self._averaged_per_cycle_time
    # endregion getters

    def pause(self):
        if DEBUG_PRINTS:
            print("Worker paused.")
        self._currently_paused = True

    def unpause(self):
        if DEBUG_PRINTS:
            print("Worker unpaused.")
        self._currently_paused = False

    def on_key_press(self, key):
        if repr(key) == repr(config.get_decrement_key()):
            self._blackscreen_counter -= 1
            if DEBUG_PRINTS:
                print("Blackscreen counter was decremented")
                print("New Blackscreen Count: " + str(self._blackscreen_counter))
            self.blackscreen_counter_updated.emit(self._blackscreen_counter)
            sleep(config.get_after_key_press_delay())
        elif repr(key) == repr(config.get_increment_key()):
            self._blackscreen_counter += 1
            if DEBUG_PRINTS:
                print("Blackscreen counter was incremented")
                print("New Blackscreen Count: " + str(self._blackscreen_counter))
            self.blackscreen_counter_updated.emit(self._blackscreen_counter)
            sleep(config.get_after_key_press_delay())
        elif repr(key) == repr(config.get_reset_key()):
            self._reset_after_this_iteration = True
            if DEBUG_PRINTS:
                print("Reset!")
                print("Wait for splitter to restart...")
            sleep(config.get_after_key_press_delay())
        elif repr(key) == repr(config.get_pause_key()):
            self.pause_status_updated.emit()
            sleep(config.get_after_key_press_delay())

    def run(self):
        if DEBUG_PRINTS:
            print("Starting splitter worker for profile " + self._splits_profile.get_name())

        # Enable Keys (Decrement, Increment, Reset, Pause)
        self._key_press_listener.start()

        # Main loop
        # NOTE: this part is HEAVILY inspired by this video by Code Bullet: https://www.youtube.com/watch?v=wHRubMACen0
        while not self._finished:
            if not self._currently_paused:
                start_time: float = time()

                img: Optional[ndarray] = self._camera.grab(region=config.get_video_preview_coords())
                if img is not None:  # image is None if nothing changed
                    current_average_gray_value: float = average_gray_value(img)

                    self.avg_grey_value_updated.emit(current_average_gray_value)
                    if DEBUG_PRINTS:
                        print("Average Grey Value: " + str(current_average_gray_value))

                    if current_average_gray_value <= config.get_blackscreen_threshold():
                        self._blackscreen_counter += 1
                        self.blackscreen_counter_updated.emit(self._blackscreen_counter)
                        if DEBUG_PRINTS:
                            print("Blackscreen Count: " + str(self._blackscreen_counter))

                        if self._blackscreen_counter in self._splits_profile.get_splits():
                            if DEBUG_PRINTS:
                                print("Pressing " + repr(config.get_split_key()))
                            self._keyboard.press(config.get_split_key())
                        sleep(config.get_after_split_delay())

                # wait if capture rate is above allowed max
                if (time() - start_time) < (1 / config.get_max_capture_rate()):
                    sleep((1 / config.get_max_capture_rate()) - (time() - start_time))

                # update per-cycle time
                per_cycle_time: float = time() - start_time
                if DEBUG_PRINTS:
                    print(f"Time per Cycle: {per_cycle_time}")  # Enable for Debug
                if self._averaged_per_cycle_time is None:
                    self._averaged_per_cycle_time = per_cycle_time
                else:
                    self._averaged_per_cycle_time = (per_cycle_time + self._averaged_per_cycle_time) / 2

            if self._reset_after_this_iteration:
                self._blackscreen_counter = 0
                self.blackscreen_counter_updated.emit(self._blackscreen_counter)
                self._reset_after_this_iteration = False
                if DEBUG_PRINTS:
                    print("Splitter reset!")

    def finish(self):
        if DEBUG_PRINTS:
            print("Worker stopped.")
        self._key_press_listener.stop()
        self._camera = None
        self._finished = True
