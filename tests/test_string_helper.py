import pytest

from pynput.keyboard import Key, KeyCode

import src.string_helper as string_helper


def test_format_key_name_case_alphanumeric():
    assert string_helper.format_key_name("\'a\'") == "A"


def test_format_key_name_case_function():
    assert string_helper.format_key_name("<Key.space: <???>>") == "SPACE"


def test_format_key_name_case_unrecognized_code():
    assert string_helper.format_key_name("<42>") == "OEM.42"


def test_format_key_name_case_none():
    assert string_helper.format_key_name("None") == "-"


def test_key_str_to_obj_case_alphanumeric():
    assert string_helper.key_str_to_obj("\'a\'") == 'a'


def test_key_str_to_obj_case_function():
    assert string_helper.key_str_to_obj("<Key.space: <???>>") == Key.space


def test_key_str_to_obj_case_unrecognized_code():
    assert string_helper.key_str_to_obj("<42>") ==  KeyCode.from_vk(42)


def test_key_str_to_obj_case_none():
    assert string_helper.key_str_to_obj(None) is None
