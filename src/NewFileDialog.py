"""(GUI) Graphical Menu for creating new splits files. """
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox


class NewFileDialog(QDialog):

    def __init__(self):
        super().__init__()

        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)

        self.setWindowTitle("New File")

        # make window as small as possible
        self.setFixedSize(self.sizeHint().width(), self.sizeHint().height())

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Enter Name of new splits file:"))
        self.layout.addWidget(QLineEdit())
        self.layout.addWidget(self._btn_box)

    def _btn_box_accepted(self):
        # TODO: Create New File with given name and check for its existance
        self.close()

    def _btn_box_rejected(self):
        self.close()
