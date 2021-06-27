# NOTE: this tool is HEAVILY inspired by this video from Code Bullet: https://www.youtube.com/watch?v=wHRubMACen0
import numpy as np
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from PIL import ImageGrab
import cv2
import time

# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
setup_at_start: bool         # Do setup at start?
split_key: str               # Key automatically pressed when valif blackscreen is detected
video_preview_coords = []    # Corners of stream preview window
splits = []                  # Blackscreen count values at which to split
blackscreen_threshold: float # Threshold for average gray value for a screen to count as blackscreen (0 by default)
max_capture_rate: int        # Times per second a capture is taken (NOTE: this is a maximum and possibly unreachable)
after_split_delay: float     # Delay to prevent multiple splits per blackscreen in seconds
decrement_key: str           # Key to press to decrement press counter after "accidental" blackscreen (i. e. death)
increment_key: str           # "Well, there's currently no cases where that's useful or important! ;)
reset_key: str               # Key to press to restart program without actually restarting
after_key_press_delay: float # Delay after any key press to prevent multiple registrations
pause_key: str               # Key to press once to pause and press again to unpause


if __name__ == '__main__':

    mouse = MouseController()
    keyboard = KeyboardController()
    preview_coord_counter = 0
    blackscreen_counter = 0
    reset_after_this_iteration = False
    currently_paused = False

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

    def on_press_decrement(key):
        global blackscreen_counter
        if repr(key) == decrement_key:
            blackscreen_counter -= 1
            print("Blackscreen counter was decremented")
            print("New Blackscreen Count: " + str(blackscreen_counter))
            time.sleep(after_key_press_delay)

    def on_press_increment(key):
        global blackscreen_counter
        if repr(key) == increment_key:
            blackscreen_counter += 1
            print("Blackscreen counter was incremented")
            print("New Blackscreen Count: " + str(blackscreen_counter))
            time.sleep(after_key_press_delay)

    def on_press_reset(key):
        global reset_after_this_iteration
        if repr(key) == reset_key:
            reset_after_this_iteration = True
            print("Reset!")
            print("Wait for splitter to restart...")
            time.sleep(after_key_press_delay)

    def on_press_pause(key):
        global currently_paused
        if repr(key) == pause_key:
            if currently_paused:
                currently_paused = False
                print("Unpaused!")
            else:
                currently_paused = True
                print("Paused...")
            time.sleep(after_key_press_delay)

    def on_press_set_split_key(key):
        global split_key
        split_key = repr(key)
        print(repr(key) + " was set as your Split key!")
        return False

    def on_press_set_decrement_key(key):
        global decrement_key
        decrement_key = repr(key)
        print(repr(key) + " was set as your Decrement key!")
        return False

    def on_press_set_increment_key(key):
        global increment_key
        increment_key = repr(key)
        print(repr(key) + " was set as your Increment key!")
        return False

    def on_press_set_reset_key(key):
        global reset_key
        reset_key = repr(key)
        print(repr(key) + " was set as your Reset key!")
        return False

    def on_press_set_pause_key(key):
        global pause_key
        pause_key = repr(key)
        print(repr(key) + " was set as your Pause key!")
        return False

    def on_click_set_coords(x, y, button, pressed):
        global video_preview_coords
        global preview_coord_counter
        if button == Button.left and pressed:
            if preview_coord_counter == 0:
                video_preview_coords[0] = x
                video_preview_coords[1] = y
                preview_coord_counter += 1
                print("First Corner was set to (" + str(x) + "," + str(y) + ")!")
            else:
                video_preview_coords[2] = x
                video_preview_coords[3] = y
                preview_coord_counter += 1
                print("Second Corner was uset to (" + str(x) + "," + str(y) + ")!")
                correct_coords()
                return False

    # Read config
    with open("config.cfg", 'r') as config_file:
        settings = config_file.readlines()
        setup_at_start = eval(settings[0])
        split_key = settings[1].split('\n')[0]
        video_preview_coords = eval(settings[2])
        blackscreen_threshold = eval(settings[3])
        max_capture_rate = eval(settings[4])
        after_split_delay = eval(settings[5])
        decrement_key = settings[6].split('\n')[0]
        increment_key = settings[7].split('\n')[0]
        reset_key = settings[8].split('\n')[0]
        after_key_press_delay = eval(settings[9])
        pause_key = settings[10].split('\n')[0]

    # Setup
    if setup_at_start:
        # Set Split Key
        print("Press the key you use for splitting:")
        with KeyboardListener(on_press=on_press_set_split_key) as keyboard_listener:
            keyboard_listener.join()

        # Set Decrement Key
        print("Press the key you want to use for manually decrementing the blackscreen counter once:")
        with KeyboardListener(on_press=on_press_set_decrement_key) as keyboard_listener:
            keyboard_listener.join()

        # Set Increment Key
        print("Press the key you want to use for manually incrementing the blackscreen counter once:")
        with KeyboardListener(on_press=on_press_set_increment_key) as keyboard_listener:
            keyboard_listener.join()

        # Set Reset Key
        print("Press the key you want to use to reset the running program:")
        with KeyboardListener(on_press=on_press_set_reset_key) as keyboard_listener:
            keyboard_listener.join()

        # Set Pause Key
        print("Press the key you want to use to pause and unpause the running program:")
        with KeyboardListener(on_press=on_press_set_pause_key) as keyboard_listener:
            keyboard_listener.join()

        # Set video preview coords
        print("Click to set video preview coords: (pick 2 diagonally opposed corners)")
        with MouseListener(on_click=on_click_set_coords) as mouse_listener:
            mouse_listener.join()

        # Set blackscreen threshold
        user_input = int(input("Set maximum grey value to still count as black: (0-255, black-white, 0 by default)\n"))
        if 0 <= user_input <= 255:
            blackscreen_threshold = user_input
        else:
            blackscreen_threshold = 0

        # Set after split delay
        user_input = int(input("Set minimum delay between splits to prevent repeated splitting on the same blackscreen: (time in seconds)\n"))
        if user_input > 0:
            after_split_delay = user_input
        else:
            after_split_delay = 10

        # Enable/Disable setup on future program starts depending on user input
        print("Setup done!")
        print("Don't forget to enter your splits manually in splits.txt!")
        user_input = input("Skip setup at future program starts? (y/n)\n")
        if user_input == "y" or user_input == "Y" or user_input == "yes":
            setup_at_start = False
        else:
            setup_at_start = True

        # Write changes to config.cfg
        with open("config.cfg", 'w') as config_file:
            config_file.write(repr(setup_at_start) + "\n")
            config_file.write(split_key + "\n")
            config_file.write(repr(video_preview_coords) + "\n")
            config_file.write(repr(blackscreen_threshold) + "\n")
            config_file.write(repr(max_capture_rate) + "\n")
            config_file.write(repr(after_split_delay) + "\n")
            config_file.write(decrement_key + "\n")
            config_file.write(increment_key + "\n")
            config_file.write(reset_key + "\n")
            config_file.write(repr(after_key_press_delay) + "\n")
            config_file.write(pause_key)

    # Read splits
    with open("splits.txt", 'r') as splits_file:
        lines = splits_file.readlines()
        for line in lines:
            if line != "" and line[0] != '#':
                splits.append(int(line.split('#')[0]))

    # Enable Keys (Decrement, Increment, Reset, Pause)
    decrement_listener = KeyboardListener(on_press=on_press_decrement)
    decrement_listener.start()
    increment_listener = KeyboardListener(on_press=on_press_increment)
    increment_listener.start()
    reset_listener = KeyboardListener(on_press=on_press_reset)
    reset_listener.start()
    pause_listener = KeyboardListener(on_press=on_press_pause)
    pause_listener.start()

    # Main loop
    while True:
        blackscreen_counter = 0
        reset_after_this_iteration = False
        print("Splitter start!")
        while not reset_after_this_iteration:
            while not currently_paused:
                start_time = time.time()

                screen = np.array(ImageGrab.grab(bbox=video_preview_coords))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                print("Average Grey Value: " + str(np.average(screen))) # Enable for Debug

                if np.average(screen) <= blackscreen_threshold:
                    blackscreen_counter += 1
                    print("Blackscreen Count: " + str(blackscreen_counter))
                    if blackscreen_counter in splits:
                        keyboard.press(eval(split_key[1:].split(':')[0]))
                    time.sleep(after_split_delay)

                # print("Time per Cycle: " + str(time.time() - start_time)) # Enable for Debug
                while (time.time() - start_time) < (1 / max_capture_rate):
                    time.sleep(0.01)
