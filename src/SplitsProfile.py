import os


def load_from_file(path: str):
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
    def __init__(self):
        self.name: str = "Unnamed Profile"
        # Blackscreen count values at which to split
        self.splits = []
