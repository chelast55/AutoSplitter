from PySide6 import QtCore, QtWidgets

# qt app needs to be constructed before we can do anything else with qt
app = QtWidgets.QApplication([])

from MainWidget import MainWidget
import Config
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener

mouse = MouseController()
keyboard = KeyboardController()

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


if __name__ == '__main__':
    widget = MainWidget()
    widget.resize(400, 150)
    widget.show()

    # exit when main window is closed
    exit(app.exec())
