"""(GUI) Graphical Menu for selecting, creating and editing splits profiles."""

from PySide6.QtGui import QFontDatabase, QSyntaxHighlighter, Qt, QTextCharFormat
from PySide6.QtWidgets import QTreeView, QFileSystemModel, QVBoxLayout, QDialog, QHBoxLayout, QTextEdit, QPushButton
import os
from src import Config
from src.NewFileDialog import NewFileDialog
from src.SplitsProfileEditorWidget import SplitsProfileEditorWidget
import json

# TODO: Save splits to new .json format
# TODO: Columns for split and split name
# TODO: Add Save button instead of live editing splits
# TODO: Incorporate "creator comments" (maybe switch between splits and comment
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

        self._splits_profile_editor: SplitsProfileEditorWidget = SplitsProfileEditorWidget()
        self._splits_profile_editor.get_splits_edit().setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        SplitsSyntaxHighlighter(self._splits_profile_editor.get_splits_edit().document())

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

        # hide all columns except for "name"
        for i in range(1, self._directory_model.columnCount()):
            self._tv_directory.hideColumn(i)

    def _btn_new_file_on_click(self):
        new_file_dialog = NewFileDialog()
        new_file_dialog.exec()

    def _btn_save_file_on_click(self):
        # TODO: save contents of SplitsProfileEditorWidget to corresponding .json file
        pass

    def _tv_directory_on_click(self):
        selected_index = self._tv_directory.selectedIndexes()[0]
        path = self._directory_model.filePath(selected_index)

        if os.path.exists(path) and os.path.isfile(path):
            self._splits_profile_editor.get_splits_edit().setText(open(path, "r").read())

    def _tv_directory_on_double_click(self):
        selected_index = self._tv_directory.selectedIndexes()[0]
        path = self._directory_model.filePath(selected_index)

        if os.path.exists(path) and os.path.isfile(path):
            Config.path_to_current_splits_profile = "splits_profiles/" + path.split("/splits_profiles/")[1]
            Config.write_config_to_file()
            self.close()
