from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QDialogButtonBox

import Config
from KeyPickerWidget import KeyPickerWidget


class SetupWidget(QWidget):

    def __init__(self):
        super(SetupWidget, self).__init__()

        self._btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.resize(250, 200)

        self._key_picker_split: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_pause: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_reset: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_decrement: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_increment: KeyPickerWidget = KeyPickerWidget()

        self._key_picker_split.set_key(Config.split_key)
        self._key_picker_pause.set_key(Config.pause_key)
        self._key_picker_reset.set_key(Config.reset_key)
        self._key_picker_decrement.set_key(Config.decrement_key)
        self._key_picker_increment.set_key(Config.increment_key)

        self.setWindowModality(Qt.ApplicationModal)
        self.layout = QVBoxLayout(self)

        settings_layout = QHBoxLayout()

        button_settings_layout = QFormLayout()
        button_settings_layout.addRow("Split Key:", self._key_picker_split)
        button_settings_layout.addRow("Pause Key:", self._key_picker_pause)
        button_settings_layout.addRow("Reset Key:", self._key_picker_reset)
        button_settings_layout.addRow("Decrement Key:", self._key_picker_decrement)
        button_settings_layout.addRow("Increment Key:", self._key_picker_increment)
        settings_layout.addLayout(button_settings_layout)

        rect_select_layout = QVBoxLayout()
        settings_layout.addLayout(rect_select_layout)

        self.layout.addLayout(settings_layout)

        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)
        self.layout.addWidget(self._btn_box)

    def _btn_box_accepted(self):
        Config.split_key = self._key_picker_split.key
        Config.pause_key = self._key_picker_pause.key
        Config.reset_key = self._key_picker_reset.key
        Config.decrement_key = self._key_picker_decrement.key
        Config.increment_key = self._key_picker_increment.key
        Config.write_config_to_file()
        self.close()

    def _btn_box_rejected(self):
        self.close()
