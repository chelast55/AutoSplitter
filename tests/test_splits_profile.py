import pytest

from os import path

from src.splits_profile import SplitsProfile

NAME: str = "example"
GAME: str = "example.exe"
CATEGORY: str = "whatever%"
AUTHOR: str = "chelast55"
VIDEO: str = "https://www.youtube.com/watch?v=o-YBDTqX_ZU"
COMMENT: str = "Shoutouts to simplefilps! Money goes to \"Kill the animals!\""
SPLITS: dict[int, str] = {
    1: "very funny split name",
    3: "next split has no name",
    5: ""
}

INDICES: list[int] = [1, 3, 5]
NAMES: list[str] = ["very funny split name", "next split has no name", ""]

SPLITS_PROFILE_PATH = path.join(path.dirname(path.abspath(__file__)), r"test_data", r"example.json")


@pytest.fixture
def _profile():
    return SplitsProfile()


########################################################################################################################
# test_get_split_indices                                                                                               #
########################################################################################################################

def test_get_split_indices(_profile):
    _profile.load_from_file(SPLITS_PROFILE_PATH)

    assert _profile.get_split_indices() == INDICES


########################################################################################################################
# test_get_split_names                                                                                                 #
########################################################################################################################

def test_get_split_names(_profile):
    _profile.load_from_file(SPLITS_PROFILE_PATH)

    assert _profile.get_split_names() == NAMES


########################################################################################################################
# test_load_from_file                                                                                                  #
########################################################################################################################

def test_load_from_file(_profile):
    _profile.load_from_file(SPLITS_PROFILE_PATH)

    assert _profile.get_name() == NAME
    assert _profile.get_game() == GAME
    assert _profile.get_category() == CATEGORY
    assert _profile.get_author() == AUTHOR
    assert _profile.get_video() == VIDEO
    assert _profile.get_comment() == COMMENT
    assert _profile.get_splits() == SPLITS
