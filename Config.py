import os.path

from pynput.keyboard import Key, KeyCode

import Config

# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
video_preview_coords = []       # Corners of stream preview window
split_key: Key = None           # Key automatically pressed when valid blackscreen is detected
pause_key: Key = None           # Key to press once to pause and press again to unpause
reset_key: Key = None           # Key to press to restart program without actually restarting
decrement_key: Key = None       # Key to press to decrement counter after "accidental" blackscreen (i. e. death)
increment_key: Key = None       # "Well, there's currently no cases where that's useful or important" ;)
blackscreen_threshold: float    # Threshold for average gray value for a screen to count as blackscreen (default 15)
after_split_delay: float        # Delay to prevent multiple splits per blackscreen in seconds
max_capture_rate: int           # Times/second a capture is taken (NOTE: this is a maximum and possibly unreachable)
after_key_press_delay: float                # Delay after any key press to prevent multiple registrations
automatic_threshold_overhead: float         # Value added to automatically calculated threshold for better tolerance
path_to_current_splits_profile: str = ""    # Path to the currently selected splits profile config file


def key_str_to_obj(s):
    if s.startswith('<'):
        if s[1] == 'K':  # function key
            return eval(s[1:].split(':')[0])
        else:  # unrecognized scan code
            return KeyCode.from_vk(int(s[1:-2]))
    else:
        return eval(s)


def read_config_from_file():
    global video_preview_coords
    global split_key, pause_key, reset_key, decrement_key, increment_key, blackscreen_threshold, after_split_delay
    global max_capture_rate, after_key_press_delay, automatic_threshold_overhead
    global path_to_current_splits_profile
    with open("config.cfg", 'r') as config_file:
        print("Loading config.")
        settings = config_file.readlines()
        video_preview_coords = eval(settings[0])
        split_key = key_str_to_obj(settings[1])
        pause_key = key_str_to_obj(settings[2])
        reset_key = key_str_to_obj(settings[3])
        decrement_key = key_str_to_obj(settings[4])
        increment_key = key_str_to_obj(settings[5])
        blackscreen_threshold = eval(settings[6])
        after_split_delay = eval(settings[7])
        max_capture_rate = eval(settings[8])
        after_key_press_delay = eval(settings[9])
        automatic_threshold_overhead = eval(settings[10])
        path_to_current_splits_profile = settings[11].split('\n')[0]


def restore_defaults():
    global video_preview_coords
    global blackscreen_threshold, after_split_delay
    global max_capture_rate, after_key_press_delay, automatic_threshold_overhead
    video_preview_coords = [1.0, 1.0, 100.0, 100.0]
    blackscreen_threshold = 9
    after_split_delay = 7
    max_capture_rate = 60
    after_key_press_delay = 3
    automatic_threshold_overhead = 3


# Executed when importing
if os.path.isfile("config.cfg"):
    read_config_from_file()
else:
    restore_defaults()


def write_config_to_file():
    # Write changes to config.cfg
    with open("config.cfg", 'w') as config_file:
        config_file.write(repr(video_preview_coords) + "\n")
        config_file.write(repr(split_key) + "\n")
        config_file.write(repr(pause_key) + "\n")
        config_file.write(repr(reset_key) + "\n")
        config_file.write(repr(decrement_key) + "\n")
        config_file.write(repr(increment_key) + "\n")
        config_file.write(repr(blackscreen_threshold) + "\n")
        config_file.write(repr(after_split_delay) + "\n")
        config_file.write(repr(max_capture_rate) + "\n")
        config_file.write(repr(after_key_press_delay) + "\n")
        config_file.write(repr(automatic_threshold_overhead) + "\n")
        config_file.write(path_to_current_splits_profile + "\n")
