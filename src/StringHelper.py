"""Helper class with methods for (re)formatting strings and converting between strings and keyboard keys"""

from pynput.keyboard import Key, KeyCode

key_name_format_dictionary = {"<Key.cmd: <91>>": "WIN_L",
                              "<Key.cmd_r: <92>>": "WIN_R",
                              "<Key.shift: <160>>": "SHIFT_L",
                              "<12>": "NUM.CENTER",
                              "<96>": "NUM.0",
                              "<97>": "NUM.1",
                              "<98>": "NUM.2",
                              "<99>": "NUM.3",
                              "<100>": "NUM.4",
                              "<101>": "NUM.5",
                              "<102>": "NUM.6",
                              "<103>": "NUM.7",
                              "<104>": "NUM.8",
                              "<105>": "NUM.9",
                              "<110>": "NUM.DOT"}
"""For reformatting string representations of certain key codes, deemed unclear for the user, to something more 
readable. """


def format_key_name(key_repr: str):
    """
    Reformats string representation of keys to something more ideal for a users understandings

    :param key_repr: (str) string representation of a key on the keyboard
    :returns: (str) formatted string
    """
    if key_repr in key_name_format_dictionary:
        return key_name_format_dictionary.get(key_repr)
    elif key_repr[0] == '<':
        if key_repr[1] == 'K':  # function key
            return key_repr[1:].split(':')[0].split('.')[1].upper()
        else:  # unrecognized scan code
            print(key_repr[1:-1])
            return "OEM." + key_repr[1:-1]
    elif key_repr[0] == 'N':  # None
        return "-"
    else:  # alphanumeric key
        return key_repr[1:-1].upper()


def key_str_to_obj(s: str) -> Key:
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
            return KeyCode.from_vk(int(s[1:-1]))
    else:
        return eval(s)
