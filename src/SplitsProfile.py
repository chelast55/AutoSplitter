"""Contains class representation of splits files and methods surrounding it"""

import os

# TODO:  rework this to .json format

def load_from_file(path: str):
    """
    Read content of splits file and load them into splits profile object.
    Each valid (non-comment) line in the file is turned into an element of the splits list in the generated splits profile object.

    If the path is invalid, the splits profile turns out empty.

    :param path: (str) file path to splits file
    :return: (SplitsProfile) object representation of read in splits file
    """
    sp = SplitsProfile()
    sp.name = os.path.basename(path)

    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r') as splits_file:
            lines = splits_file.readlines()
            for line in lines:
                if line != "" and line[0] != '#':
                    sp.splits.append(int(line.split('#')[0]))
    return sp


class SplitsProfile:
    """Class representation of splits file"""
    def __init__(self):
        self.name: str = "Unnamed Profile"
        """Name of the splits profile"""
        self.splits = []
        """List of all blackscreen count values where an automatic split is supposed to happen"""
