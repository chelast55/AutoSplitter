import pytest

from os import path, rename, remove
from pynput.keyboard import KeyCode

import src.config as config


SPLITS_PROFILE_PATH = path.join(path.dirname(path.abspath(__file__)), r"test_data", r"example.json")

SOME_SETTINGS: dict[str, any] = {"global": [
    {
        "video_preview_coords": (1.0, 1.0, 100.0, 100.0),
        "split_key": 'a',
        "pause_key": 'Key.space',
        "reset_key": 'b',
        "decrement_key": repr(KeyCode.from_vk(42)),
        "increment_key": None,
        "blackscreen_threshold": 9,
        "after_split_delay": 7,
        "max_capture_rate": 60,
        "after_key_press_delay": 0.2,
        "automatic_threshold_overhead": 3
    }
], "path_to_current_splits_profile": SPLITS_PROFILE_PATH}


########################################################################################################################
# test_read_global_config_from_file                                                                                    #
########################################################################################################################

def test_read_global_config_from_file():
    _store_config_file()

    config._global_settings = SOME_SETTINGS
    config.write_config_to_file()
    config._global_settings = None

    config.read_global_config_from_file()

    _restore_config_file()

    assert config.get_global_settings() == SOME_SETTINGS


########################################################################################################################
# test_read_per_profile_config_from_file                                                                               #
########################################################################################################################

def test_read_per_profile_config_from_file_case_splits_profile_selected():
    config._global_settings["path_to_current_splits_profile"] = SOME_SETTINGS["path_to_current_splits_profile"]
    config._per_profile_settings = None

    config.read_per_profile_config_from_file()

    assert config.get_per_profile_settings()["video_preview_coords"] == (42, 42, 99, 99)
    assert config.get_per_profile_settings()["split_key"] == "Key.space"

    assert config.get_video_preview_coords() == (42, 42, 99, 99)
    # config.get_split_key() is not tested to remove dependency on string_helper.py


def test_read_per_profile_config_from_file_case_no_splits_profile_selected():
    config.read_per_profile_config_from_file()

    assert True # no errors


########################################################################################################################
# test_write_config_to_file                                                                                            #
########################################################################################################################

def test_write_config_to_file():
    _store_config_file()

    config._global_settings = SOME_SETTINGS
    config.write_config_to_file()

    _restore_config_file()

    assert config.get_global_settings() == SOME_SETTINGS


########################################################################################################################
# test_delete_config_file                                                                                              #
########################################################################################################################

def test_delete_config_file_case_file_exists():
    _store_config_file()

    with open(config.get_config_file_path(), 'w+') as config_file:
        config_file.write("Yee")

    config.delete_config_file()
    exists: bool = path.exists(config.get_config_file_path())

    _restore_config_file()

    assert exists is False


def test_delete_config_file_case_file_not_exists():
    _store_config_file()

    config.delete_config_file()
    exists: bool = path.exists(config.get_config_file_path())

    _restore_config_file()

    assert exists is False


########################################################################################################################
# test_restore_defaults                                                                                                #
########################################################################################################################

def test_restore_defaults():
    config._global_settings = None

    config.restore_defaults()

    assert config.get_global_settings() == config.get_default_settings()


########################################################################################################################
# test_on_import                                                                                                       #
########################################################################################################################

def test_on_import_case_config_does_exist():
    _store_config_file()

    config._global_settings = SOME_SETTINGS
    config.write_config_to_file()
    config._global_settings = None
    config._per_profile_settings = None

    config._on_import()

    _restore_config_file()

    assert config.get_global_settings() == SOME_SETTINGS
    assert config.get_per_profile_settings()["split_key"] == "Key.space"


def test_on_import_case_config_does_not_exist():
    _store_config_file()

    config._global_settings = None
    config._per_profile_settings = None

    config._on_import()

    _restore_config_file()

    assert config.get_global_settings() == config.get_default_settings()


########################################################################################################################
# helpers                                                                                                              #
########################################################################################################################

def _store_config_file():
    if path.isfile(config.get_config_file_path()):
        rename(config.get_config_file_path(), config.get_config_file_path() + ".temp")


def _restore_config_file():
    if path.isfile(config.get_config_file_path()):
        remove(config.get_config_file_path())
    if path.isfile(config.get_config_file_path() + ".temp"):
        rename(config.get_config_file_path() + ".temp", config.get_config_file_path())
