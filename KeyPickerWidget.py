from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QDialog, QVBoxLayout, QDialogButtonBox, \
    QSizePolicy
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
import StringHelper


class KeyPickerDialog(QDialog):

    def __init__(self):
        super().__init__()

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
        self._lbl = QLabel("-")
        self._btn = QPushButton("Set")
        self._btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self._dialog = None

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self._lbl)
        self.layout.addWidget(self._btn)
        self._btn.clicked.connect(self._btn_on_click)

    def _btn_on_click(self):
        dialog = KeyPickerDialog()

        if dialog.exec() == QDialog.Accepted:
            self.set_key(dialog.selected_key)

    def set_key(self, key):
        self.key = key
        self._lbl.setText(StringHelper.format_key_name(repr(key)))
