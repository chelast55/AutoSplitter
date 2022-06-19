"""Contains class representation of splits files and methods surrounding it"""
import json
import os


class SplitsProfile:
    """Class representation of splits file"""

    def __init__(self):
        self.name: str = "Unnamed Profile"
        """Name of the splits profile"""
        self.splits = {}
        """List of splits consisting of touples of (index, split name)"""

    def get_split_indices(self):
        """:return: Get list of blackscreen count values where an automatic split is supposed to happen"""
        indices = []
        for split in self.splits:
            indices.append(split)
        return indices

    def get_split_names(self):
        """:return: Get list of names of all valid blackscreen counts"""
        names = []
        for split in self.splits:
            names.append(self.splits.get(split))
        return names

    def name_of_split(self, c: int):
        """
        :param c: (int) blackscreen count of split
        :return: name of split corresponding to c
        """
        return self.splits.get(c)


def load_from_file(path: str) -> SplitsProfile:
    """
    Read content of splits file and load them into splits profile object.
    Each valid (non-comment) line in the file is turned into an element of the splits list in the generated splits profile object.

    If the path is invalid, the splits profile turns out empty.

    :param path: (str) file path to splits file
    :return: (SplitsProfile) object representation of read in splits file
    """
    sp = SplitsProfile()
    sp.name = os.path.basename(path)[:-5]

    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r') as splits_file:
            file_content = json.load(splits_file)
            lines = file_content.get(sp.name + "_splits")[0].get("splits")
            for line in lines:
                sp.splits[int(line[0])] = str(line[1])
    return sp
