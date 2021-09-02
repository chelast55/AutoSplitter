"""(GUI) Graphical Menu for editing splits files. It has separate sections for editing metadata (game, category,
author) and splits with split names. """

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QSizePolicy, QLayout, \
    QFormLayout


class SplitsProfileEditorWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._le_game: QLineEdit = QLineEdit()
        self._le_category: QLineEdit = QLineEdit()
        self._le_author: QLineEdit = QLineEdit()
        self._le_video: QLineEdit = QLineEdit()
        self._te_splits: QTextEdit = QTextEdit()
        self._te_splits.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.layout = QVBoxLayout(self)
        items_layout = QFormLayout()
        items_layout.addRow("Game: ", self._le_game)
        items_layout.addRow("Category:", self._le_category)
        items_layout.addRow("Author:", self._le_author)
        items_layout.addRow("Video:", self._le_video)
        self.layout.addLayout(items_layout)
        self.layout.addWidget(self._te_splits)

    def get_game(self):
        return self._le_game.text()

    def get_category(self):
        return self._le_category.text()

    def get_author(self):
        return self._le_author.text()

    def get_video(self):
        return self._le_video.text()

    def get_splits_edit(self):
        return self._te_splits
