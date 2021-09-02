"""(GUI) Graphical Menu for editing splits files. It has separate sections for editing metadata (game, category,
author) and splits with split names. """
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit


class SplitsProfileEditorWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._mi_game: MetadataItemWidget = MetadataItemWidget("Game:")
        self._mi_category: MetadataItemWidget = MetadataItemWidget("Category:")
        self._mi_author: MetadataItemWidget = MetadataItemWidget("Author:")
        self._mi_video: MetadataItemWidget = MetadataItemWidget("Video:")
        self._te_splits: QTextEdit = QTextEdit()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._mi_game)
        self.layout.addWidget(self._mi_category)
        self.layout.addWidget(self._mi_author)
        self.layout.addWidget(self._mi_video)
        self.layout.addWidget(self._te_splits)

    def get_game(self):
        return self._mi_game.line_edit.text()

    def get_category(self):
        return self._mi_category.line_edit.text()

    def get_author(self):
        return self._mi_author.line_edit.text()

    def get_video(self):
        return self._mi_video.line_edit.text()

    def get_splits_edit(self):
        return self._te_splits


class MetadataItemWidget(QWidget):
    def __init__(self, item: str):
        super().__init__()

        self.line_edit: QLineEdit = QLineEdit()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(QLabel(item))
        self.layout.addWidget(self.line_edit)
