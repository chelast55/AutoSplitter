from typing import Optional

from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThread
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout

import SplitsProfile
from ScreenWatchWorker import ScreenWatchWorker


class MainWidget(QWidget):
    _workerThread: Optional[QThread] = None
    _worker: Optional[ScreenWatchWorker] = None

    _btn_start_stop: QPushButton = None
    _lbl_selected_profile: QLabel

    def __init__(self):
        super().__init__()

        self.text = QLabel("Hello World",
                           alignment=QtCore.Qt.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)

        self._btn_start_stop = QPushButton("Start")
        self.layout.addWidget(self._btn_start_stop)

        self._btn_start_stop.clicked.connect(self._btn_start_stop_on_click)

    def _btn_start_stop_on_click(self):
        # if worker is not started start it, otherwise stop it
        if self._worker is None:
            self._start_worker()
            self._btn_start_stop.setText("Stop")
        else:
            self._stop_worker()
            self._btn_start_stop.setText("Start")

    def _start_worker(self):
        self._workerThread = QtCore.QThread()
        self._worker = ScreenWatchWorker(SplitsProfile.load_from_file("splits.txt"))
        self._worker.moveToThread(self._workerThread)
        self._workerThread.started.connect(self._worker.run)
        self._workerThread.start()

    def _stop_worker(self):
        if self._worker is not None:
            self._worker.finish()
        self._worker = None

        if self._workerThread is not None:
            self._workerThread.quit()
            self._workerThread.wait()
        self._workerThread = None

    def closeEvent(self, event: QCloseEvent):
        self._stop_worker()
