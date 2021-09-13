"""(GUI) Graphical Menu for selecting, creating and editing splits profiles."""

from PySide6.QtGui import QFontDatabase, QSyntaxHighlighter, Qt, QTextCharFormat
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QVBoxLayout, QDialog, QHBoxLayout, QTextEdit, QPushButton, \
    QTableWidgetItem
import os
from src import Config
from src.NewFileDialog import NewFileDialog
from src.SplitsProfileEditorWidget import SplitsProfileEditorWidget
import json
from pynput.keyboard import Key, Listener as KeyboardListener


# TODO: Consider sorting in directories automatically based on game tag


class SplitsSyntaxHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text: str) -> None:
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

        self.setWindowTitle("Splits Profile")
        self.resize(720, 480)

        self.layout = QHBoxLayout(self)
        main_layout = QVBoxLayout()
        self._tv_directory: QTreeView = QTreeView()
        main_layout.addWidget(self._tv_directory)
        # TODO: Find a more robust way to get the splits_profiles directory (seriously, do that!)
        splits_profiles_dir: str = os.path.join(os.getcwd(), "splits_profiles")
        self._directory_model: QFileSystemModel = QFileSystemModel()
        self._directory_model.setRootPath(splits_profiles_dir)
        self._tv_directory.setModel(self._directory_model)
        self._tv_directory.setRootIndex(self._directory_model.index(splits_profiles_dir))
        self._tv_directory.clicked.connect(self._tv_directory_on_click)
        self._tv_directory.doubleClicked.connect(self._tv_directory_on_double_click)

        self._table_resize_listener = KeyboardListener(on_press=self._on_table_resize_trigger)
        self._table_resize_listener.start()
        self._held_toggle_listener = KeyboardListener(on_press=self._on_held_toggle_press,
                                                      on_release=self._on_held_toggle_release)
        self._held_toggle_listener.start()
        self._shift_held: bool = False

        self._splits_profile_editor: SplitsProfileEditorWidget = SplitsProfileEditorWidget()
        # self._splits_profile_editor.te_splits.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        # SplitsSyntaxHighlighter(self._splits_profile_editor.te_splits.document())

        self._btn_new_file: QPushButton = QPushButton("New Splits Profile")
        self._btn_new_file.clicked.connect(self._btn_new_file_on_click)
        self._btn_save_file: QPushButton = QPushButton("Save Splits Profile")
        self._btn_save_file.clicked.connect(self._btn_save_file_on_click)

        file_button_layout = QHBoxLayout()
        file_button_layout.addWidget(self._btn_new_file)
        file_button_layout.addWidget(self._btn_save_file)
        main_layout.addLayout(file_button_layout)
        self.layout.addLayout(main_layout)
        self.layout.addWidget(self._splits_profile_editor)
        self._btn_new_file.setFocusPolicy(Qt.NoFocus)  # for better table editing
        self._btn_save_file.setFocusPolicy(Qt.NoFocus)  # for better table editing
        # TODO: add hotkeys for STRG+N and STRG+S (and possible hotkey for switching splits/comment)

        # hide all columns except for "name"
        for i in range(1, self._directory_model.columnCount()):
            self._tv_directory.hideColumn(i)

    def _btn_new_file_on_click(self):
        new_file_dialog = NewFileDialog()
        new_file_dialog.exec()

    def _btn_save_file_on_click(self):
        # TODO: change to currently selected filepath or auto-sort to fitting filepath
        profile_file_name = "yee"  # TODO: figure this out
        splits_list = []
        for i in range(0, self._splits_profile_editor.tb_splits.rowCount()):
            splits_list.append(
                (self._splits_profile_editor.tb_splits.item(i, 0).text(),
                 self._splits_profile_editor.tb_splits.item(i, 1).text()))
        with open(profile_file_name + ".json", 'w') as config_file:
            settings = {profile_file_name + "_splits": [], profile_file_name + "_settings_override": []}
            settings[profile_file_name + "_splits"].append({
                "game": self._splits_profile_editor.get_game(),
                "category": self._splits_profile_editor.get_category(),
                "author": self._splits_profile_editor.get_author(),
                "video": self._splits_profile_editor.get_video(),
                "comment": self._splits_profile_editor.get_comment(),
                "splits": splits_list})
            json.dump(settings, config_file, indent=4)
        pass

    def _tv_directory_on_click(self):
        selected_index = self._tv_directory.selectedIndexes()[0]
        path = self._directory_model.filePath(selected_index)
        profile_name = os.path.basename(path)[:-5]

        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'r') as splits_file:
                file_content = json.load(splits_file)
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

    def _tv_directory_on_double_click(self):
        selected_index = self._tv_directory.selectedIndexes()[0]
        path = self._directory_model.filePath(selected_index)

        if os.path.exists(path) and os.path.isfile(path):
            Config.path_to_current_splits_profile = "splits_profiles/" + path.split("/splits_profiles/")[1]
            Config.write_config_to_file()
            self._table_resize_listener.stop()
            self._held_toggle_listener.stop()
            self.close()

    def _on_table_resize_trigger(self, key: Key):
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
