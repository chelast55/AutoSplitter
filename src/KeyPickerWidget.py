from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QDialog, QVBoxLayout, QSizePolicy
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from src import StringHelper


class KeyPickerDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Key")
        self.selected_key: Key = None

        self._keyboard = KeyboardController()

        # make window as small as possible
        self.setFixedSize(self.sizeHint().width(), self.sizeHint().height())

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Press the key you want to set."))

        self._key_press_listener = KeyboardListener(on_press=self._on_key_press)
        self._key_press_listener.start()

    def _on_key_press(self, key):
        self.selected_key = key
        self._key_press_listener.stop()
        self.accept()


class KeyPickerWidget(QWidget):

    def __init__(self):
        super(KeyPickerWidget, self).__init__()

        self.key: Key = None
        self.key_override: Key = None
        self._lbl_global = QLabel("-")
        self._lbl_override = QLabel("-")
        self._lbl_override.setStyleSheet("color: green")

        self._btn = QPushButton("Set")
        self._btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self._dialog = None

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self._lbl_global)
        self.layout.addWidget(self._lbl_override)
        self.layout.addWidget(self._btn)
        self._btn.clicked.connect(self._btn_on_click)

    def _btn_on_click(self):
        dialog = KeyPickerDialog()

        if dialog.exec() == QDialog.Accepted:
            self.set_key(dialog.selected_key)

    def set_key(self, key):
        self.key = key
        self._lbl_global.setText(StringHelper.format_key_name(repr(key)))

    def set_key_override(self, key):
        self.key = key
        self._lbl_global.setText(StringHelper.format_key_name(repr(key)))

    def get_button(self):
        return self._btn

    def get_key(self):
        if self.key_override is not None:
            return self.key_override
        else:
            return self.key
