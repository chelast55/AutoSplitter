"""Helper class with methods for (re)formatting strings"""

key_name_format_dictionary = {}  # TODO: use this for replacing inconvenient string representations


def format_key_name(key_repr: str):
    """
    Reformats string representation of keys to something more ideal for a users understandings

    :param key_repr: (str) string representation of a key on the keyboard
    :returns: (str) formatted string
    """
    if key_repr[0] == '<':
        if key_repr[1] == 'K':  # function key
            return key_repr[1:].split(':')[0].split('.')[1].upper()
        else:  # unrecognized scan code
            print(key_repr[1:-1])
            return "OEM." + key_repr[1:-1]
    else:  # alphanumeric key
        return key_repr.upper()
