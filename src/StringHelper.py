key_name_format_dictionary = {}


def format_key_name(key_repr: str):
    if key_repr[0] == '<':
        if key_repr[1] == 'K':  # function key
            return key_repr[1:].split(':')[0].split('.')[1].upper()
        else:                   # unrecognized scan code
            print(key_repr[1:-1])
            return "OEM." + key_repr[1:-1]
    else:                       # alphanumeric key
        return key_repr.upper()
