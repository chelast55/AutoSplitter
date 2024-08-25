"""(GUI) Graphical Menu for creating new splits files. """

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
from pathlib import Path
from json import dump as json_dump


class NewFileDialog(QDialog):

    def __init__(self, path: Path):
        super().__init__()

        self._new_file_parent_path: Path = path

        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)
        self._lb_info: QLabel = QLabel("Enter Name of new splits file:\n")
        self._le_filename: QLineEdit = QLineEdit()
        self._le_filename.textChanged.connect(self._le_filename_on_text_changed)

        self.setWindowTitle("New File")

        # make window as small as possible
        self.setFixedSize(self.sizeHint().width(), self.sizeHint().height())

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._lb_info)
        self._layout.addWidget(self._le_filename)
        self._layout.addWidget(self._btn_box)

    def _btn_box_accepted(self):
        if self._new_file_parent_path.exists():
            new_file_path: Path = self._new_file_parent_path / Path(self._le_filename.text() + ".json")
            if not new_file_path.exists():
                with open(new_file_path, 'w') as config_file:
                    settings: dict = {
                        self._le_filename.text() + "_splits": [],
                        self._le_filename.text() + "_settings_override": []
                    }
                    settings[self._le_filename.text() + "_splits"].append({
                        "game": "",
                        "category": "",
                        "author": "",
                        "video": "",
                        "comment": "",
                        "splits": [["", ""]]})
                    json_dump(settings, config_file, indent=4)
                self.close()
            else:
                self._lb_info.setText("Invalid file name, file already exists.\nTry another name:")
                self._lb_info.setStyleSheet("color: red")

    def _btn_box_rejected(self):
        self.close()

    def _le_filename_on_text_changed(self):
        self._lb_info.setText("Enter Name of new splits file:\n")
        self._lb_info.setStyleSheet("color: black")
