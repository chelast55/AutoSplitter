from os import system
from shutil import rmtree, copytree
from pathlib import Path

REPO_ROOT_PATH: Path = Path(__file__).parent.resolve()
BUILD_PATH: Path = REPO_ROOT_PATH / "build"
DIST_PATH: Path = REPO_ROOT_PATH / "dist"
MAIN_PATH: Path = REPO_ROOT_PATH / "auto_splitter.py"
SPLITS_PROFILE_SRC_PATH: Path = REPO_ROOT_PATH / "splits_profiles"
SPLITS_PROFILE_DEST_PATH: Path = DIST_PATH / "auto_splitter" / "splits_profiles"


if __name__ == "__main__":
    # cleenup
    if BUILD_PATH.exists():
        rmtree(BUILD_PATH)
    if DIST_PATH.exists():
        rmtree(DIST_PATH)

    # build executable
    BUILD_PATH.mkdir()
    system("cd build")
    system("pyinstaller " + str(MAIN_PATH))

    # copy splits_profiles dir
    copytree(SPLITS_PROFILE_SRC_PATH, SPLITS_PROFILE_DEST_PATH)
