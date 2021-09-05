"""
Handles reading from and writing to the config file (config.json).
Stores configuration parameters internally and publicly accessible.
"""

import os.path
import json

from pynput.keyboard import Key, KeyCode

# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
video_preview_coords = []
"""Corners of area of the screen the program observes for blackscreens"""
split_key: Key = None
"""Key automatically pressed when valid blackscreen is detected"""
pause_key: Key = None
"""Key to press once to pause and press again to unpause"""
reset_key: Key = None
"""Key to press to restart program without actually restarting"""
decrement_key: Key = None
"""Key to press to decrement counter after "accidental" blackscreen (i. e. death)"""
increment_key: Key = None
""""Well, there's currently no cases where that's useful or important" ;)"""
blackscreen_threshold: float
"""Threshold for average gray value for a screen to count as blackscreen (default 15)"""
after_split_delay: float
"""Delay to prevent multiple splits per blackscreen in seconds"""
max_capture_rate: int
"""Times/second a capture is taken (NOTE: this is a maximum and possibly unreachable)"""
after_key_press_delay: float
"""Delay after any key press to prevent multiple registrations"""
automatic_threshold_overhead: float
"""Value added to automatically calculated threshold for better tolerance"""
path_to_current_splits_profile: str = ""
"""Path to the currently selected splits profile config file"""


def key_str_to_obj(s):
    """
    Get key object from string representation.

    Note, that this is NOT its string representation obtainable via repr(). Simply using repr() would not work,
    because repr() of function keys (which intern are enum states) do not translate to key objects by themself.

    :param s: (str) "string representation"
    :return: (key) key object
    """
    if s.startswith('<'):
        if s[1] == 'K':  # function key
            return eval(s[1:].split(':')[0])
        else:  # unrecognized scan code
            return KeyCode.from_vk(int(s[1:-2]))
    else:
        return eval(s)


def read_config_from_file():
    """
    Read all config parameters from file (config.json) and store them internally.

    Whenever a new config paramter is introduced, a new line for it should be added to the end of this method.
    """
    global video_preview_coords
    global split_key, pause_key, reset_key, decrement_key, increment_key, blackscreen_threshold, after_split_delay
    global max_capture_rate, after_key_press_delay, automatic_threshold_overhead
    global path_to_current_splits_profile
    with open("config.json", 'r') as config_file:
        settings = json.load(config_file).get("global")[0]
        video_preview_coords = settings.get("video_preview_coords")
        split_key = key_str_to_obj(settings.get("split_key"))
        pause_key = key_str_to_obj(settings.get("pause_key"))
        reset_key = key_str_to_obj(settings.get("reset_key"))
        decrement_key = key_str_to_obj(settings.get("decrement_key"))
        increment_key = key_str_to_obj(settings.get("increment_key"))
        blackscreen_threshold = settings.get("blackscreen_threshold")
        after_split_delay = settings.get("after_split_delay")
        max_capture_rate = settings.get("max_capture_rate")
        after_key_press_delay = settings.get("after_key_press_delay")
        automatic_threshold_overhead = settings.get("automatic_threshold_overhead")
        path_to_current_splits_profile = settings.get("path_to_current_splits_profile")


def restore_defaults():
    """
    Overwrite currently stored config parameters with their default values without updating config.json

    This method serves as baseline for what is considered "default".
    """
    global video_preview_coords
    global blackscreen_threshold, after_split_delay
    global max_capture_rate, after_key_press_delay, automatic_threshold_overhead
    video_preview_coords = [1.0, 1.0, 100.0, 100.0]
    blackscreen_threshold = 9
    after_split_delay = 7
    max_capture_rate = 60
    after_key_press_delay = 1
    automatic_threshold_overhead = 3


# Executed when importing
if os.path.isfile("config.json"):
    read_config_from_file()
else:
    restore_defaults()


def write_config_to_file():
    """
    Write all internally stored config parameters to file (config.json).

    Whenever a new config parameter is introduced, a new line for it should be added to the end of settings.
    """
    with open("config.json", 'w') as config_file:
        settings = {"global": []}
        settings["global"].append({
            "video_preview_coords": video_preview_coords,
            "split_key": repr(split_key),
            "pause_key": repr(pause_key),
            "reset_key": repr(reset_key),
            "decrement_key": repr(decrement_key),
            "increment_key": repr(increment_key),
            "blackscreen_threshold": blackscreen_threshold,
            "after_split_delay": after_split_delay,
            "max_capture_rate": max_capture_rate,
            "after_key_press_delay": after_key_press_delay,
            "automatic_threshold_overhead": automatic_threshold_overhead,
            "path_to_current_splits_profile": path_to_current_splits_profile})
        json.dump(settings, config_file, indent=4)
