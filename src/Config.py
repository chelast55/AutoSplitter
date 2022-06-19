"""
Handles reading from and writing to the config file (config.json).
Stores configuration parameters internally and publicly accessible.
"""

import os.path
import json
import time

from PySide6.QtWidgets import QMessageBox
from pynput.keyboard import Key

from src.StringHelper import key_str_to_obj


_config_file_path: str = os.path.dirname(os.path.abspath(__file__))[:-3] + "config.json"
"""Path to global config file"""

_global_settings = {}
"""Global Settings stored in .json format"""

_per_profile_settings = {}
"""Per-Profile Settings of currently loaded splits file stored in .json format"""


########################################################################################################################
# Getters for settings                                                                                                 #
#                                                                                                                      #
# For key codes see https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key                          #
########################################################################################################################

def get_video_preview_coords() -> []:
    """Corners of area of the screen the program observes for blackscreens"""
    if "video_preview_coords" in _per_profile_settings:
        return _per_profile_settings.get("video_preview_coords")
    else:
        return _global_settings.get("global")[0].get("video_preview_coords")


def get_split_key() -> Key:
    """Key automatically pressed when valid blackscreen is detected"""
    if "split_key" in _per_profile_settings:
        return key_str_to_obj(_per_profile_settings.get("split_key"))
    else:
        return key_str_to_obj(_global_settings.get("global")[0].get("split_key"))


def get_pause_key() -> Key:
    """Key to press once to pause and press again to unpause"""
    if "pause_key" in _per_profile_settings:
        return key_str_to_obj(_per_profile_settings.get("pause_key"))
    else:
        return key_str_to_obj(_global_settings.get("global")[0].get("pause_key"))


def get_reset_key() -> Key:
    """Key to press to restart program without actually restarting"""
    if "reset_key" in _per_profile_settings:
        return key_str_to_obj(_per_profile_settings.get("reset_key"))
    else:
        return key_str_to_obj(_global_settings.get("global")[0].get("reset_key"))


def get_decrement_key() -> Key:
    """Key to press to decrement counter after "accidental" blackscreen (i. e. death)"""
    if "decrement_key" in _per_profile_settings:
        return key_str_to_obj(_per_profile_settings.get("decrement_key"))
    else:
        return key_str_to_obj(_global_settings.get("global")[0].get("decrement_key"))


def get_increment_key() -> Key:
    """"Well, there's currently no cases where that's useful or important" (except for pause/decrement user error)"""
    if "increment_key" in _per_profile_settings:
        return key_str_to_obj(_per_profile_settings.get("increment_key"))
    else:
        return key_str_to_obj(_global_settings.get("global")[0].get("increment_key"))


def get_blackscreen_threshold() -> float:
    """Threshold for average gray value for a screen to count as blackscreen (default 15)"""
    if "blackscreen_threshold" in _per_profile_settings:
        return _per_profile_settings.get("blackscreen_threshold")
    else:
        return _global_settings.get("global")[0].get("blackscreen_threshold")


def get_after_split_delay() -> float:
    """Delay to prevent multiple splits per blackscreen in seconds"""
    if "after_split_delay" in _per_profile_settings:
        return _per_profile_settings.get("after_split_delay")
    else:
        return _global_settings.get("global")[0].get("after_split_delay")


def get_max_capture_rate() -> float:
    """Times/second a capture is taken (NOTE: this is a maximum and possibly unreachable)"""
    if "max_capture_rate" in _per_profile_settings:
        return _per_profile_settings.get("max_capture_rate")
    else:
        return _global_settings.get("global")[0].get("max_capture_rate")


def get_after_key_press_delay() -> float:
    """Delay after any key press to prevent multiple registrations"""
    if "after_key_press_delay" in _per_profile_settings:
        return _per_profile_settings.get("after_key_press_delay")
    else:
        return _global_settings.get("global")[0].get("after_key_press_delay")


def get_automatic_threshold_overhead() -> float:
    """Value added to automatically calculated threshold for better tolerance"""
    if "after_key_press_delay" in _per_profile_settings:
        return _per_profile_settings.get("automatic_threshold_overhead")
    else:
        return _global_settings.get("global")[0].get("automatic_threshold_overhead")


def get_current_splits_profile_path() -> str:
    """Path to the currently selected splits profile config file"""
    return _global_settings.get("path_to_current_splits_profile")


########################################################################################################################
# Setters for global settings                                                                                          #
########################################################################################################################

def set_video_preview_coords(coords):
    """Corners of area of the screen the program observes for blackscreens"""
    _global_settings.get("global")[0]["video_preview_coords"] = coords


def set_split_key(split_key : Key):
    """Key automatically pressed when valid blackscreen is detected"""
    _global_settings.get("global")[0]["split_key"] = split_key


def set_pause_key(pause_key : Key):
    """Key to press once to pause and press again to unpause"""
    _global_settings.get("global")[0]["pause_key"] = pause_key


def set_reset_key(reset_key : Key):
    """Key to press to restart program without actually restarting"""
    _global_settings.get("global")[0]["reset_key"] = reset_key


def set_decrement_key(decrement_key : Key):
    """Key to press to decrement counter after "accidental" blackscreen (i. e. death)"""
    _global_settings.get("global")[0]["decrement_key"] = decrement_key


def set_increment_key(increment_key : Key):
    """"Well, there's currently no cases where that's useful or important" (except for pause/decrement user error)"""
    _global_settings.get("global")[0]["increment_key"] = increment_key


def set_blackscreen_threshold(blackscreen_threshold : float):
    """Threshold for average gray value for a screen to count as blackscreen (default 15)"""
    _global_settings.get("global")[0]["blackscreen_threshold"] = blackscreen_threshold


def set_after_split_delay(after_split_delay : float):
    """Delay to prevent multiple splits per blackscreen in seconds"""
    _global_settings.get("global")[0]["after_split_delay"] = after_split_delay


def set_max_capture_rate(max_capture_rate : float):
    """Times/second a capture is taken (NOTE: this is a maximum and possibly unreachable)"""
    _global_settings.get("global")[0]["max_capture_rate"] = max_capture_rate


def set_after_key_press_delay(after_key_press_delay : float):
    """Delay after any key press to prevent multiple registrations"""
    _global_settings.get("global")[0]["after_key_press_delay"] = after_key_press_delay


def set_automatic_threshold_overhead(automatic_threshold_overhead : float):
    """Value added to automatically calculated threshold for better tolerance"""
    _global_settings.get("global")[0]["automatic_threshold_overhead"] = automatic_threshold_overhead


def set_current_splits_profile_path(path : str):
    """Path to the currently selected splits profile config file"""
    _global_settings["path_to_current_splits_profile"] = path


########################################################################################################################
# Config Read/Write/Delete/Restore                                                                                     #
########################################################################################################################

def read_global_config_from_file():
    """
    Read all global config parameters from file (config.json) and store them internally.

    Whenever a new config paramter is introduced, a new line for it should be added to the end of this method.
    """
    global _global_settings
    try:
        with open(_config_file_path, 'r') as config_file:
            _global_settings = json.load(config_file)
    except (json.decoder.JSONDecodeError, AttributeError):
        msg_splits_file_format_error: QMessageBox = QMessageBox()
        msg_splits_file_format_error.setIcon(QMessageBox.Critical)
        msg_splits_file_format_error.setWindowTitle("config format error")
        msg_splits_file_format_error.setText("Could not load config because config.json is invalid.\nDo you want to "
                                             "delete config.json?")
        msg_splits_file_format_error.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_splits_file_format_error.button(QMessageBox.Yes).clicked.connect(delete_config_file)
        msg_splits_file_format_error.button(QMessageBox.No).clicked.connect(read_global_config_from_file)
        msg_splits_file_format_error.exec()
        while msg_splits_file_format_error.isVisible():
            time.sleep(1)
        restore_defaults()


def read_per_profile_config_from_file():
    """
    Read all per-profile setting overrides from current splits profile and override the internal settings.

    Whenever a new config parameter is introduced, a new line for it should be added to the end of this method.
    """
    global _per_profile_settings
    if not get_current_splits_profile_path() == "":
        try:
            print(get_current_splits_profile_path())
            with open(get_current_splits_profile_path(), 'r') as splits_profile:
                _per_profile_settings = json.load(splits_profile).get(
                    os.path.basename(get_current_splits_profile_path())[:-5] + "_settings_override")
        except (json.decoder.JSONDecodeError, AttributeError):
            msg_splits_file_format_error: QMessageBox = QMessageBox()
            msg_splits_file_format_error.setIcon(QMessageBox.Critical)
            msg_splits_file_format_error.setWindowTitle("config format error")
            msg_splits_file_format_error.setText(
                "Could not load config because"
                + os.path.basename(get_current_splits_profile_path())
                + " is invalid.")
            msg_splits_file_format_error.exec()
            current_splits_profile_path = ""
            write_config_to_file()


def write_config_to_file():
    """
    Write all internally stored config parameters to file (config.json).

    Whenever a new config parameter is introduced, a new line for it should be added to the end of settings.
    """
    with open(_config_file_path, 'w') as config_file:
        global _global_settings
        json.dump(_global_settings, config_file, indent=4)


def delete_config_file():
    """
    Deletes config.json.
    """
    if os.path.exists(_config_file_path):
        os.remove(_config_file_path)


def restore_defaults():
    """
    Overwrite currently stored config parameters with their default values without updating config.json

    This method serves as baseline for what is considered "default".
    """
    global _global_settings
    _global_settings = {"global": [], "path_to_current_splits_profile": ""}
    _global_settings["global"].append({
        "video_preview_coords": [1.0, 1.0, 100.0, 100.0],
        "split_key": repr(None),
        "pause_key": repr(None),
        "reset_key": repr(None),
        "decrement_key": repr(None),
        "increment_key": repr(None),
        "blackscreen_threshold": 9,
        "after_split_delay": 7,
        "max_capture_rate": 60,
        "after_key_press_delay": 0.2,
        "automatic_threshold_overhead": 3})


########################################################################################################################
# Executed when importing                                                                                              #
########################################################################################################################

if os.path.isfile(_config_file_path):
    read_global_config_from_file()
    read_per_profile_config_from_file()
else:
    restore_defaults()
