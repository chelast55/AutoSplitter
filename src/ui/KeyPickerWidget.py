"""Widget containing a button that opens a dialog for registering keyboard keys and two labels to display these keys"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QDialog, QVBoxLayout, QSizePolicy, \
    QPushButton
from pynput.keyboard import Key, Listener as KeyboardListener

from src.string_helper import format_key_name


class KeyPickerDialog(QDialog):
    """Dialog that asks for a key press and returns this selected key when accepted"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Key")

        self._selected_key: Key = None

        # make window as small as possible
        self.setFixedSize(self.sizeHint().width(), self.sizeHint().height())

        # layout
        self._layout: QVBoxLayout = QVBoxLayout(self)
        self._layout.addWidget(QLabel("Press the key you want to set."))

        # keyboard listener
        self._key_press_listener: KeyboardListener = KeyboardListener(on_press=self._on_key_press)
        self._key_press_listener.start()

        # virtual button for closing/accepting
        self._virtual_button: QPushButton = QPushButton()
        self._virtual_button.clicked.connect(self.accept)

    ########################
    # Button functionality #
    ########################

    def _on_key_press(self, key):
        self._selected_key = key
        self._key_press_listener.stop()
        # Yes, this is (seemingly) necessary, because calling accept() directly somehow causes an infinite loop
        self._virtual_button.click()

    ###########
    # Getters #
    ###########

    def get_selected_key(self) -> Key:
        return self._selected_key


class KeyPickerWidget(QWidget):
    """Widget containing a button that opens a dialog for registering keyboard keys and two labels to display these
    keys """

    def __init__(self):
        super(KeyPickerWidget, self).__init__()

        self._global_key: Key = None
        self._override_key: Key = None

        # layout
        self._lbl_global: QLabel = QLabel("-")
        self._lbl_override: QLabel = QLabel("-")
        self._btn: QPushButton = QPushButton("Set")

        self._lbl_override.setStyleSheet("color: green")
        self._btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

        self._layout = QHBoxLayout(self)
        self._layout.addWidget(self._lbl_global)
        self._layout.addWidget(self._lbl_override)
        self._layout.addWidget(self._btn)

        # connect functionality to buttons
        self._btn.clicked.connect(self._btn_on_click)

    ###########
    # Getters #
    ###########

    def get_button(self):
        return self._btn

    def get_global_key(self):
        return self._global_key

    def get_override_key(self):
        return self._override_key

    ###########
    # Setters #
    ###########

    def set_key(self, key):
        self._global_key = key
        self._lbl_global.setText(format_key_name(repr(key)))

    def set_key_override(self, key):
        self._override_key = key
        self._lbl_global.setText(format_key_name(repr(key)))

    ########################
    # Button functionality #
    ########################
    # TODO: figure out how to set overrides
    def _btn_on_click(self):
        dialog: KeyPickerDialog = KeyPickerDialog()

        if dialog.exec() == QDialog.Accepted:
            self.set_key(dialog.get_selected_key())
