from os import system
import random
from PySide6 import QtWidgets, QtCore

import SplitsProfile
from ScreenWatchWorker import ScreenWatchWorker


class MainWidget(QtWidgets.QWidget):
    
    threadPool: QtCore.QThreadPool = None

    def __init__(self):
        super().__init__()

        self.threadPool = QtCore.QThreadPool()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        worker = ScreenWatchWorker(SplitsProfile.load_from_file("splits.txt"))
        self.threadPool.start(worker)
