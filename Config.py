from pynput.keyboard import Key


def key_str_to_obj(s):
    if s.startswith('<'):
        return eval(s[1:].split(':')[0])
    else:
        return eval(s)


# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
setup_at_start: bool            # Do setup at start?
split_key = None                # Key automatically pressed when valid blackscreen is detected
video_preview_coords = []       # Corners of stream preview window
blackscreen_threshold: float    # Threshold for average gray value for a screen to count as blackscreen (0 by default)
max_capture_rate: int           # Times per second a capture is taken (NOTE: this is a maximum and possibly unreachable)
after_split_delay: float        # Delay to prevent multiple splits per blackscreen in seconds
decrement_key: str              # Key to press to decrement press counter after "accidental" blackscreen (i. e. death)
increment_key: str              # "Well, there's currently no cases where that's useful or important" ;)
reset_key: str                  # Key to press to restart program without actually restarting
after_key_press_delay: float    # Delay after any key press to prevent multiple registrations
pause_key: str                  # Key to press once to pause and press again to unpause

with open("config.cfg", 'r') as config_file:
    print("Loading config.")
    settings = config_file.readlines()
    setup_at_start = eval(settings[0])
    split_key = key_str_to_obj(settings[1])
    video_preview_coords = eval(settings[2])
    blackscreen_threshold = eval(settings[3])
    max_capture_rate = eval(settings[4])
    after_split_delay = eval(settings[5])
    decrement_key = key_str_to_obj(settings[6])
    increment_key = key_str_to_obj(settings[7])
    reset_key = key_str_to_obj(settings[8])
    after_key_press_delay = eval(settings[9])
    pause_key = key_str_to_obj(settings[10])


def write_config_to_file():
    # Write changes to config.cfg
    with open("config.cfg", 'w') as config_file:
        config_file.write(repr(setup_at_start) + "\n")
        config_file.write(repr(split_key) + "\n")
        config_file.write(repr(video_preview_coords) + "\n")
        config_file.write(repr(blackscreen_threshold) + "\n")
        config_file.write(repr(max_capture_rate) + "\n")
        config_file.write(repr(after_split_delay) + "\n")
        config_file.write(decrement_key + "\n")
        config_file.write(increment_key + "\n")
        config_file.write(reset_key + "\n")
        config_file.write(repr(after_key_press_delay) + "\n")
        config_file.write(pause_key)