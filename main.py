from PySide6 import QtCore, QtWidgets

# qt app needs to be constructed before we can do anything else with qt
app = QtWidgets.QApplication([])

from MainWidget import MainWidget
import Config
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener



preview_coord_counter = 0
mouse = MouseController()
keyboard = KeyboardController()


def correct_coords():
    # check x coords
    if Config.video_preview_coords[2] < Config.video_preview_coords[0]:
        # swap x1 and x2
        temp = Config.video_preview_coords[0]
        Config.video_preview_coords[0] = Config.video_preview_coords[2]
        Config.video_preview_coords[2] = temp
    elif Config.video_preview_coords[2] == Config.video_preview_coords[0]:
        Config.video_preview_coords[2] += 1

    # check y coords
    if Config.video_preview_coords[3] < Config.video_preview_coords[1]:
        # swap y1 and y2
        temp = Config.video_preview_coords[1]
        Config.video_preview_coords[1] = Config.video_preview_coords[3]
        Config.video_preview_coords[3] = temp
    elif Config.video_preview_coords[3] == Config.video_preview_coords[1]:
        Config.video_preview_coords[3] += 1


def on_press_set_split_key(key: Key):
    Config.split_key = key
    print(repr(key) + " was set as your Split key!")
    return False


def on_press_set_decrement_key(key):
    Config.decrement_key = repr(key)
    print(repr(key) + " was set as your Decrement key!")
    return False


def on_press_set_increment_key(key):
    Config.increment_key = repr(key)
    print(repr(key) + " was set as your Increment key!")
    return False


def on_press_set_reset_key(key):
    Config.reset_key = repr(key)
    print(repr(key) + " was set as your Reset key!")
    return False


def on_press_set_pause_key(key):
    Config.pause_key = repr(key)
    print(repr(key) + " was set as your Pause key!")
    return False


def on_click_set_coords(x, y, button, pressed):
    global preview_coord_counter
    if button == Button.left and pressed:
        if preview_coord_counter == 0:
            Config.video_preview_coords[0] = x
            Config.video_preview_coords[1] = y
            preview_coord_counter += 1
            print("First Corner was set to (" + str(x) + "," + str(y) + ")!")
        else:
            Config.video_preview_coords[2] = x
            Config.video_preview_coords[3] = y
            preview_coord_counter += 1
            print("Second Corner was uset to (" + str(x) + "," + str(y) + ")!")
            correct_coords()
            return False


def run_setup():
    # Set video preview coords
    print("Click to set video preview coords: (pick 2 diagonally opposed corners)")
    with MouseListener(on_click=on_click_set_coords) as mouse_listener:
        mouse_listener.join()

    # Enable/Disable setup on future program starts depending on user input
    print("Setup done!")
    print("Don't forget to enter your splits manually in splits.txt!")
    user_input = input("Skip setup at future program starts? (y/n)\n")
    if user_input == "y" or user_input == "Y" or user_input == "yes":
        Config.setup_at_start = False
    else:
        Config.setup_at_start = True
        
    Config.write_config_to_file()


if __name__ == '__main__':
    if Config.setup_at_start:
        run_setup()

    widget = MainWidget()
    widget.resize(400, 150)
    widget.show()

    # exit when main window is closed
    exit(app.exec())
