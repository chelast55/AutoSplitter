"""(GUI) Graphical Menu for selecting, creating and editing splits profiles."""

from pynput.keyboard import Key, Listener as KeyboardListener
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QSyntaxHighlighter, Qt, QTextCharFormat, QShortcut, QKeySequence, QCloseEvent
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QVBoxLayout, QDialog, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QMessageBox
from pathlib import Path
from json import dump as json_dump, load as json_load
from json.decoder import JSONDecodeError
from typing import Any, Optional


from src import config
from src.ui.NewFileDialog import NewFileDialog
from src.ui.SplitsProfileEditorWidget import SplitsProfileEditorWidget


# TODO: Consider sorting in directories automatically based on game tag


class SplitsSyntaxHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text: str) -> None:
        """
        TODO: document
        :param text:
        :return:
        """
        # loop through the characters in the line
        for i in range(len(text)):
            # if we find a # the rest of the line is a comment. Format it with the comment style and return; we don't
            # need to check the rest of the line, it's a comment anyway
            if text[i] == "#":
                text_format: QTextCharFormat = QTextCharFormat()
                text_format.setForeground(Qt.gray)
                text_format.setFontItalic(True)
                self.setFormat(i, len(text) - i, text_format)
                return
            elif not text[i].isdigit():
                # if a character is not a digit check that after it only spaces or # (comment signs) follow
                if text[i].isspace():
                    inner_i = i
                    while inner_i < len(text) - 1 and text[inner_i].isspace():
                        inner_i += 1

                    if text[inner_i] != "#" and not text[inner_i].isspace():
                        text_format: QTextCharFormat = QTextCharFormat()
                        text_format.setUnderlineColor(Qt.red)
                        text_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
                        self.setFormat(i, len(text) - i, text_format)
                else:
                    # if the character is not a digit nor a space it has to be an invalid character
                    text_format: QTextCharFormat = QTextCharFormat()
                    text_format.setUnderlineColor(Qt.red)
                    text_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
                    self.setFormat(i, len(text) - i, text_format)


class SplitsProfileSelectorDialog(QDialog):

    def __init__(self):
        super().__init__()

        # Workaround until handled properly for .exe
        internal_path: Path = Path(__file__).parent.parent.parent.parent.resolve() / "_internal"
        if internal_path.is_dir():
            splits_profiles_new_path: Path = internal_path.parent / "splits_profiles"
            splits_profiles_new_path.mkdir(exist_ok=True)
            with open(splits_profiles_new_path / "example.json", "w+") as example_file:
                example_file.write(
                    """
                    {
                        \"example_splits\": [
                            {
                                \"game\": \"example.exe\",
                                \"category\": \"whatever%\",
                                \"author\": \"chelast55\",
                                \"video\": \"https://www.youtube.com/watch?v=o-YBDTqX_ZU\",
                                \"comment\": \"Shoutouts to simplefilps! Money goes to \\\"Kill the animals!\\\"\",
                                \"splits\": [
                                    [
                                        1,
                                        \"very funny split name\"
                                    ],
                                    [
                                        3,
                                        \"next split has no name\"
                                    ],
                                    [
                                        5,
                                        \"\"
                                    ]
                                ]
                            }
                        ],
                        \"example_settings_override\": []
                    }
                    """
                )


        # Window Setup
        self.setWindowTitle("Splits Profile")
        self.resize(720, 480)

        # Layout
        self._layout: QHBoxLayout = QHBoxLayout(self)
        _main_layout: QVBoxLayout = QVBoxLayout()
        self._tv_directory: QTreeView = QTreeView()
        _main_layout.addWidget(self._tv_directory)
        self._splits_profiles_dir: Path = splits_profiles_new_path # Path(__file__).parent.parent.parent.resolve() / Path("splits_profiles")

        self._directory_model: QFileSystemModel = QFileSystemModel()
        self._directory_model.setRootPath(str(self._splits_profiles_dir))
        self._tv_directory.setModel(self._directory_model)
        self._tv_directory.setRootIndex(self._directory_model.index(str(self._splits_profiles_dir)))
        self._btn_new_file: QPushButton = QPushButton("New Splits Profile")
        self._btn_save_file: QPushButton = QPushButton("Save Splits Profile")
        self._shortcut_new: QShortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self._shortcut_save: QShortcut = QShortcut(QKeySequence("Ctrl+S"), self)

        _file_button_layout: QHBoxLayout = QHBoxLayout()
        _file_button_layout.addWidget(self._btn_new_file)
        _file_button_layout.addWidget(self._btn_save_file)
        _main_layout.addLayout(_file_button_layout)
        self._layout.addLayout(_main_layout)
        self._btn_new_file.setFocusPolicy(Qt.NoFocus)  # for better table editing
        self._btn_save_file.setFocusPolicy(Qt.NoFocus)  # for better table editing

        self._splits_profile_editor: SplitsProfileEditorWidget = SplitsProfileEditorWidget()
        self._layout.addWidget(self._splits_profile_editor)

        # misc. visual setup
        for i in range(1, self._directory_model.columnCount()):
            self._tv_directory.hideColumn(i)  # hide all columns (name, size, file format, etc.) except for "name"

        # connect functionality to buttons
        self._tv_directory.clicked.connect(self._tv_directory_on_click)
        self._tv_directory.doubleClicked.connect(self._tv_directory_on_double_click)
        self._btn_new_file.clicked.connect(self._btn_new_file_on_click)
        self._btn_save_file.clicked.connect(self._btn_save_file_on_click)
        self._shortcut_new.activated.connect(self._btn_new_file_on_click)
        self._shortcut_save.activated.connect(self._btn_save_file_on_click)

        # Background tasks
        self._table_resize_listener: KeyboardListener = KeyboardListener(on_press=self._on_table_resize_trigger)
        self._table_resize_listener.start()
        self._held_toggle_listener: KeyboardListener = KeyboardListener(on_press=self._on_held_toggle_press,
                                                                        on_release=self._on_held_toggle_release)
        self._held_toggle_listener.start()
        self._shift_held: bool = False

        self._unchanged_settings: dict = {}

    def get_current_settings(self) -> dict:
        settings: dict = {}
        if len(self._tv_directory.selectedIndexes()) > 0:
            selected_index: QModelIndex = self._tv_directory.selectedIndexes()[0]
            path: Path = self._splits_profile_editor.opened_file_path
            profile_name: str = path.stem.split(".json")[0]
            splits_list: list[tuple[str, str]] = []

            for i in range(0, self._splits_profile_editor.tb_splits.rowCount()):
                row_blackscreen_count: Optional[str] = None
                if self._splits_profile_editor.tb_splits.item(i, 0) is not None:
                    row_blackscreen_count = self._splits_profile_editor.tb_splits.item(i, 0).text()
                row_split_name: Optional[str] = None
                if self._splits_profile_editor.tb_splits.item(i, 1) is not None:
                    row_split_name = self._splits_profile_editor.tb_splits.item(i, 1).text()
                splits_list.append((row_blackscreen_count, row_split_name))

            settings = {profile_name + "_splits": [], profile_name + "_settings_override": []}
            settings[profile_name + "_splits"].append({
                "game": self._splits_profile_editor.get_game(),
                "category": self._splits_profile_editor.get_category(),
                "author": self._splits_profile_editor.get_author(),
                "video": self._splits_profile_editor.get_video(),
                "comment": self._splits_profile_editor.get_comment(),
                "splits": splits_list})
        return settings

    def _btn_new_file_on_click(self):
        if len(self._tv_directory.selectedIndexes()) > 0:
            selected_index: QModelIndex = self._tv_directory.selectedIndexes()[0]
            new_file_parent_path: Path = Path(self._directory_model.filePath(selected_index))
            if new_file_parent_path.is_file():
                new_file_parent_path = new_file_parent_path.parent
        else:
            new_file_parent_path: Path = self._splits_profiles_dir

        new_file_dialog: NewFileDialog = NewFileDialog(new_file_parent_path)
        new_file_dialog.exec()

    def _btn_save_file_on_click(self):
        if self._splits_profile_editor.opened_file_path not in [None, Path("")]:
            path: Path = self._splits_profile_editor.opened_file_path
            profile_name: str = path.stem.split(".json")[0]

            # check if all blackscreen count values are integers
            settings: dict = self.get_current_settings()
            splits_list: list[tuple[Any, Any]] = settings[profile_name + "_splits"][0]["splits"]
            for i in range(len(splits_list)):
                try:
                    splits_list[i] = (int(splits_list[i][0]), splits_list[i][1])
                except (TypeError, ValueError):
                    blackscreen_count_value_error: QMessageBox = QMessageBox()
                    blackscreen_count_value_error.setIcon(QMessageBox.Critical)
                    blackscreen_count_value_error.setWindowTitle("Value Error in blacksreens column")
                    blackscreen_count_value_error.setText(
                        f"Saving splits failed :/\n"
                        f"blackscreen count in row {i + 1} is not a number:"
                        f"\n{splits_list[i][0] if not splits_list[i][0] in [None, ""] else "<empty>"}")
                    blackscreen_count_value_error.setStandardButtons(QMessageBox.Ok)
                    blackscreen_count_value_error.exec()
                    return

            with open(self._splits_profiles_dir / Path(profile_name + ".json"), 'w+') as config_file:
                json_dump(settings, config_file, indent=4)
                self._unchanged_settings = self.get_current_settings()

    def _tv_directory_on_click(self):
        selected_index: QModelIndex = self._tv_directory.selectedIndexes()[0]
        path: Path = Path(self._directory_model.filePath(selected_index))
        profile_name: str = path.stem.split(".json")[0]

        if path.exists() and path.is_file():

            # check if there are any pending changes
            if (
                    self._splits_profile_editor.opened_file_path != Path("")
                    and self.get_current_settings() != self._unchanged_settings
            ):
                splits_profile_save_reminder: QMessageBox = QMessageBox()
                splits_profile_save_reminder.setIcon(QMessageBox.Question)
                splits_profile_save_reminder.setWindowTitle("Save splits profile changes?")
                splits_profile_save_reminder.setText("Do you want to save the changes to your current splits profile?")
                splits_profile_save_reminder.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
                splits_profile_save_reminder.setDefaultButton(QMessageBox.Save)
                splits_profile_save_reminder.button(QMessageBox.Save).clicked.connect(self._btn_save_file_on_click)
                splits_profile_save_reminder.exec()

            try:
                with open(path, 'r') as splits_file:
                    file_content: dict[Any] = json_load(splits_file)
                    self._splits_profile_editor.le_game.setText(file_content.get(profile_name + "_splits")[0].get("game"))
                    self._splits_profile_editor.le_category.setText(
                        file_content.get(profile_name + "_splits")[0].get("category"))
                    self._splits_profile_editor.le_author.setText(
                        file_content.get(profile_name + "_splits")[0].get("author"))
                    self._splits_profile_editor.le_video.setText(file_content.get(profile_name + "_splits")[0].get("video"))
                    self._splits_profile_editor.te_comment.setText(
                        file_content.get(profile_name + "_splits")[0].get("comment"))
                    splits_list = file_content.get(profile_name + "_splits")[0].get("splits")
                    self._splits_profile_editor.tb_splits.setRowCount(len(splits_list))
                    for i in range(0, len(splits_list)):
                        self._splits_profile_editor.tb_splits.setItem(i, 0, QTableWidgetItem(str(splits_list[i][0])))
                        self._splits_profile_editor.tb_splits.setItem(i, 1, QTableWidgetItem(splits_list[i][1]))

                # only executed when no prior .json errors occurred
                self._splits_profile_editor.opened_file_path = path
                self._unchanged_settings = self.get_current_settings()
            except (JSONDecodeError, AttributeError, TypeError):
                msg_splits_file_format_error: QMessageBox = QMessageBox()
                msg_splits_file_format_error.setIcon(QMessageBox.Critical)
                msg_splits_file_format_error.setWindowTitle("Format Error in splits file")
                msg_splits_file_format_error.setText(f"Selected file at \"{path}\" does not contain a valid splits "
                                                     f"profile. Could not load splits.")
                msg_splits_file_format_error.setStandardButtons(QMessageBox.Ok)
                msg_splits_file_format_error.exec()

    def _tv_directory_on_double_click(self):
        selected_index: QModelIndex = self._tv_directory.selectedIndexes()[0]
        path: Path = Path(self._directory_model.filePath(selected_index))

        if path.exists() and path.is_file() and path == self._splits_profile_editor.opened_file_path:

            config.set_current_splits_profile_path(path)
            config.read_per_profile_config_from_file()
            config.write_config_to_file()
            config.read_current_splits_profile()
            self._table_resize_listener.stop()
            self._held_toggle_listener.stop()
            self.close()

    def _on_table_resize_trigger(self, key: Key):
        if self.isActiveWindow():
            if key == Key.tab and not self._shift_held:  # add new row at end
                if (self._splits_profile_editor.tb_splits.currentRow() == (self._splits_profile_editor.tb_splits.rowCount() - 1)) \
                        and (self._splits_profile_editor.tb_splits.currentColumn() == 1):
                    self._splits_profile_editor.tb_splits.insertRow(self._splits_profile_editor.tb_splits.rowCount())
            elif key == Key.enter:  # add new row below currently selected row
                self._splits_profile_editor.tb_splits.insertRow(self._splits_profile_editor.tb_splits.currentRow() + 1)
                self._splits_profile_editor.tb_splits.selectRow(self._splits_profile_editor.tb_splits.currentRow() + 1)
            elif key == Key.backspace or key == Key.delete:  # delete empty row
                current_row_index = self._splits_profile_editor.tb_splits.currentRow()
                if (self._splits_profile_editor.tb_splits.item(current_row_index, 0) is None
                    or self._splits_profile_editor.tb_splits.item(current_row_index, 0).text() == "") \
                        and (self._splits_profile_editor.tb_splits.item(current_row_index, 1) is None
                             or self._splits_profile_editor.tb_splits.item(current_row_index, 1).text() == ""):
                    self._splits_profile_editor.tb_splits.removeRow(current_row_index)
                    if self._splits_profile_editor.tb_splits.rowCount() == 0:
                        self._splits_profile_editor.tb_splits.setRowCount(1)
                    self._splits_profile_editor.tb_splits.selectRow(max((current_row_index - 1), 1))

    def _on_held_toggle_press(self, key: Key):
        if key == Key.shift or key == Key.shift_r:
            self._shift_held = True

    def _on_held_toggle_release(self, key: Key):
        if key == Key.shift or key == Key.shift_r:
            self._shift_held = False
