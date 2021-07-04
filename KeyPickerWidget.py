from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QDialog, QVBoxLayout, QDialogButtonBox
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener


class KeyPickerDialog(QDialog):
    selected_key: Key = None

    _keyboard = None
    _key_press_listener = None
    _lbl_key: QLabel = QLabel("Pressed Key: -")
    _btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

    def __init__(self):
        super().__init__()

        self._keyboard = KeyboardController()

        # make window as small as possible
        self.setFixedSize(self.sizeHint().width(), self.sizeHint().height())

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Press the key you want to set."))
        self.layout.addWidget(self._lbl_key)

        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)
        self.layout.addWidget(self._btn_box)

        self._key_press_listener = KeyboardListener(on_press=self._on_key_press)
        self._key_press_listener.start()

    def _btn_box_rejected(self):
        self._key_press_listener.stop()
        self.reject()

    def _btn_box_accepted(self):
        self._key_press_listener.stop()
        self.accept()

    def _on_key_press(self, key):
        self.selected_key = key
        self._lbl_key.setText("Pressed Key: " + repr(key))


class KeyPickerWidget(QWidget):
    key: Key = None

    _lbl = QLabel("-")
    _btn = QPushButton("Set")
    _dialog = None

    def __init__(self):
        super().__init__()

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
        self._lbl.setText(repr(key))
