"""(GUI) Graphical Menu for creating new splits files. """

import json
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox


class NewFileDialog(QDialog):

    def __init__(self, path: str):
        super().__init__()

        self._new_file_path: str = os.path.dirname(path) if os.path.isfile(path) else path

        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)
        self._lb_info: QLabel = QLabel("Enter Name of new splits file:\n")
        self._le_filename: QLineEdit = QLineEdit()
        self._le_filename.textChanged.connect(self._le_filename_on_text_changed)

        self.setWindowTitle("New File")

        # make window as small as possible
        self.setFixedSize(self.sizeHint().width(), self.sizeHint().height())

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._lb_info)
        self.layout.addWidget(self._le_filename)
        self.layout.addWidget(self._btn_box)

    def _btn_box_accepted(self):
        if os.path.exists(self._new_file_path):
            if not os.path.exists(self._new_file_path + '\\' + self._le_filename.text() + ".json"):
                with open(self._new_file_path + "\\" + self._le_filename.text() + ".json", 'w') as config_file:
                    settings = {self._le_filename.text() + "_splits": [],
                                self._le_filename.text() + "_settings_override": []}
                    settings[self._le_filename.text() + "_splits"].append({
                        "game": "",
                        "category": "",
                        "author": "",
                        "video": "",
                        "comment": "",
                        "splits": [["", ""]]})
                    json.dump(settings, config_file, indent=4)
                self.close()
            else:
                self._lb_info.setText("Invalid file name, file already exists.\nTry another name:")
                self._lb_info.setStyleSheet("color: red")

    def _btn_box_rejected(self):
        self.close()

    def _le_filename_on_text_changed(self):
        self._lb_info.setText("Enter Name of new splits file:\n")
        self._lb_info.setStyleSheet("color: black")
