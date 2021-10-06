"""(GUI) Graphical Menu for editing splits files. It has separate sections for editing metadata (game, category,
author) and splits with split names. """
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QSizePolicy, \
    QFormLayout, QPushButton, QTableWidget, QTableWidgetItem, QAbstractScrollArea


class SplitsProfileEditorWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.le_game: QLineEdit = QLineEdit()
        self.le_category: QLineEdit = QLineEdit()
        self.le_author: QLineEdit = QLineEdit()
        self.le_video: QLineEdit = QLineEdit()
        self._btn_switch: QPushButton = QPushButton("Edit Comment")
        self.tb_splits: QTableWidget = QTableWidget()
        self.tb_splits.setAlternatingRowColors(True)
        self.tb_splits.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.tb_splits.setColumnCount(2)
        self.tb_splits.setRowCount(5)
        self.tb_splits.setHorizontalHeaderItem(0, QTableWidgetItem("split"))
        self.tb_splits.setHorizontalHeaderItem(1, QTableWidgetItem("name"))
        self.tb_splits.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tb_splits.resizeColumnToContents(0)
        self.tb_splits.horizontalHeader().setStretchLastSection(True)
        self.te_comment: QTextEdit = QTextEdit()
        self.te_comment.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.opened_file_path: str = ""

        self.layout = QVBoxLayout(self)
        items_layout = QFormLayout()
        items_layout.addRow("Game: ", self.le_game)
        items_layout.addRow("Category:", self.le_category)
        items_layout.addRow("Author:", self.le_author)
        items_layout.addRow("Video:", self.le_video)
        self.layout.addLayout(items_layout)
        self.layout.addWidget(self._btn_switch)
        self.layout.addWidget(self.tb_splits)
        self.layout.addWidget(self.te_comment)
        self.te_comment.setVisible(False)

        self._btn_switch.clicked.connect(self._btn_on_click_switch)
        self._btn_switch.setFocusPolicy(Qt.NoFocus)  # for better table editing

    def _btn_on_click_switch(self):
        if self.tb_splits.isVisible():
            self.tb_splits.setVisible(False)
            self.te_comment.setVisible(True)
            self._btn_switch.setText("Edit Splits")
        else:
            self.te_comment.setVisible(False)
            self.tb_splits.setVisible(True)
            self._btn_switch.setText("Edit Comment")

    def get_game(self):
        return self.le_game.text()

    def get_category(self):
        return self.le_category.text()

    def get_author(self):
        return self.le_author.text()

    def get_video(self):
        return self.le_video.text()

    def get_comment(self):
        return self.te_comment.toPlainText()
