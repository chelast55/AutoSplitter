import os


def load_from_file(path: str):
    sp = SplitsProfile()
    sp.name = os.path.basename(path)
    
    with open(path, 'r') as splits_file:
        lines = splits_file.readlines()
        for line in lines:
            if line != "" and line[0] != '#':
                sp.splits.append(int(line.split('#')[0]))
    return sp


class SplitsProfile:
    name: str = "Unnamed Profile"
    splits = []                  # Blackscreen count values at which to split
