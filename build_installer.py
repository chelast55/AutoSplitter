from os import system, path, makedirs
from shutil import rmtree
from platform import system as identify_os

if identify_os() == "Windows":
    from win32com.client import Dispatch

BUILD_PATH: str = path.join(path.dirname(path.abspath(__file__)), r"build")
DIST_PATH: str = path.join(path.dirname(path.abspath(__file__)), r"dist")
MAIN_PATH: str = path.join(path.dirname(path.abspath(__file__)), r"auto_splitter.py")
EXECUTABLE_PATH: str = path.join(DIST_PATH, r"auto_splitter", "auto_splitter.exe")

if __name__ == "__main__":
    # cleenup
    if path.exists(BUILD_PATH):
        rmtree(BUILD_PATH)
    if path.exists(DIST_PATH):
        rmtree(DIST_PATH)

    # build executable
    makedirs(BUILD_PATH)
    system("cd build")
    system("pyinstaller " + MAIN_PATH)

    # create link to executable
    if identify_os() == "Windows":
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path.join(path.dirname(path.abspath(__file__)), "AutoSplitter.lnk"))
        shortcut.Targetpath = EXECUTABLE_PATH
        shortcut.WorkingDirectory = path.join(path.dirname(path.abspath(__file__)))
        shortcut.IconLocation = EXECUTABLE_PATH
        shortcut.save()
    elif identify_os() == "Darwin":  # MacOS
        pass  # TODO: implement
    elif identify_os() == "Linux":
        pass  # TODO: implement
