from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout

from KeyPickerWidget import KeyPickerWidget


class SetupWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowModality(Qt.ApplicationModal)
        self.layout = QHBoxLayout(self)
        settings_layout = QFormLayout()
        self.layout.addLayout(settings_layout)
        settings_layout.addWidget(KeyPickerWidget())

        rect_select_layout = QVBoxLayout()
        self.layout.addLayout(rect_select_layout)
