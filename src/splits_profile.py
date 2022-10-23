"""Contains class representation of splits files and methods surrounding it"""
import json
import os

from PySide6.QtWidgets import QMessageBox


class SplitsProfile:
    """Class representation of splits file"""

    def __init__(self):
        self._name: str = ""
        """Name of the splits profile"""
        self._profile: dict[str, any] = {}
        """Splits Profile stored in .json format"""

    ###########
    # Getters #
    ###########

    def get_name(self) -> str:
        """:return: Name of the splits profile"""
        return self._name

    def get_game(self) -> str:
        """:return: Game represented in the splits profile"""
        return self._profile[self._name + "_splits"][0]["game"]

    def get_category(self) -> str:
        """:return: Speedrun category represented in the splits profile"""
        return self._profile[self._name + "_splits"][0]["category"]

    def get_author(self) -> str:
        """:return: Author of the splits profile"""
        return self._profile[self._name + "_splits"][0]["author"]

    def get_video(self) -> str:
        """:return: Video example for the speedrun route represented in the splits profile"""
        return self._profile[self._name + "_splits"][0]["video"]

    def get_comment(self) -> str:
        """:return: Comment on the splits profile"""
        return self._profile[self._name + "_splits"][0]["comment"]

    def get_splits(self) -> dict[int, str]:
        """:return: List of splits consisting of touples of (index, split name)"""
        splits: dict[int, str] = {}
        for split in self._profile[self._name + "_splits"][0]["splits"]:
            splits[split[0]] = split[1]
        return splits

    def get_split_indices(self) -> list[int]:
        """:return: Get list of blackscreen count values where an automatic split is supposed to happen"""
        return list(self.get_splits().keys())

    def get_split_names(self) -> list[str]:
        """:return: Get list of names of all valid blackscreen counts"""
        return list(self.get_splits().values())

    def get_name_of_split(self, c: int) -> str:
        """
        :param c: (int) blackscreen count of split
        :return: name of split corresponding to c
        """
        return self.get_splits().get(c)

    #########
    # Other #
    #########

    def load_from_file(self, path: str):
        """
        Read content of splits file and load them into splits profile object.
        Each valid (non-comment) line in the file is turned into an element of the splits list in the generated splits profile object.
        If the path is invalid, the splits profile turns out empty.
        :param path: (str) file path to splits file
        :return: (SplitsProfile) object representation of read in splits file
        """
        self._name = os.path.basename(path)[:-5]

        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'r') as splits_file:
                self._profile = json.load(splits_file)
        # TODO: message box when JSONDecodeError
        # TODO: add validity check
