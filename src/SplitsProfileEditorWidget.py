"""(GUI) Graphical Menu for editing splits files. It has separate sections for editing metadata (game, category,
author) and splits with split names. """

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QSizePolicy, QLayout, \
    QFormLayout


class SplitsProfileEditorWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.le_game: QLineEdit = QLineEdit()
        self.le_category: QLineEdit = QLineEdit()
        self.le_author: QLineEdit = QLineEdit()
        self.le_video: QLineEdit = QLineEdit()
        self.te_splits: QTextEdit = QTextEdit()
        self.te_splits.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.layout = QVBoxLayout(self)
        items_layout = QFormLayout()
        items_layout.addRow("Game: ", self.le_game)
        items_layout.addRow("Category:", self.le_category)
        items_layout.addRow("Author:", self.le_author)
        items_layout.addRow("Video:", self.le_video)
        self.layout.addLayout(items_layout)
        self.layout.addWidget(self.te_splits)

    def get_game(self):
        return self.le_game.text()

    def get_category(self):
        return self.le_category.text()

    def get_author(self):
        return self.le_author.text()

    def get_video(self):
        return self.le_video.text()
