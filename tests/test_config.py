import pytest

from os import path, rename, remove
from pynput.keyboard import KeyCode

import src.config as config


SPLITS_PROFILE_PATH = path.join(r"test_data", r"example.json")

SOME_SETTINGS: dict[str, any] = {"global": [
    {
        "video_preview_coords": [1.0, 1.0, 100.0, 100.0],
        "split_key": 'a',
        "pause_key": 'Key.space',
        "reset_key": 'b',
        "decrement_key": None,
        "increment_key": None,
        "blackscreen_threshold": 9,
        "after_split_delay": 7,
        "max_capture_rate": 60,
        "after_key_press_delay": 0.2,
        "automatic_threshold_overhead": 3
    }
], "path_to_current_splits_profile": path.join(path.dirname(path.abspath(__file__)), SPLITS_PROFILE_PATH)}


def _store_config_file():
    if path.isfile(config.get_config_file_path()):
        rename(config.get_config_file_path(), config.get_config_file_path() + ".temp")


def _restore_config_file():
    if path.isfile(config.get_config_file_path()):
        remove(config.get_config_file_path())
    if path.isfile(config.get_config_file_path() + ".temp"):
        rename(config.get_config_file_path() + ".temp", config.get_config_file_path())


def test_on_import_case_config_does_exist():
    _store_config_file()

    config._global_settings = SOME_SETTINGS
    config.write_config_to_file()

    config._on_import()

    _restore_config_file()

    assert config.get_global_settings() == SOME_SETTINGS
    assert config.get_per_profile_settings()[0]["split_key"] == "Key.space"


def test_on_import_case_config_does_not_exist():
    _store_config_file()

    config._on_import()

    _restore_config_file()

    assert config.get_global_settings() == config.get_default_settings()


def test_jgjgkjhgkjhgkjgh():
    assert True

