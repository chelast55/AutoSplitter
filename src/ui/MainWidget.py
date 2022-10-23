from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QThread
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

#from src import Config
#from src import SplitsProfile
#from src.ScreenWatchWorker import ScreenWatchWorker
#from src.SetupWidget import SetupWidget
#from src.SplitsProfileSelectorDialog import SplitsProfileSelectorDialog


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        # layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addLayout(self._construct_main_layout())
        self.layout.addLayout(self._construct_splits_profiles_layout())
        self.layout.addLayout(self._construct_buttons_layout())

        # misc visual
        self.setWindowTitle("Blackscreen Autosplitter")
        #self._update_lbl_current_splits_profile()

        # connect functionality to buttons
        #self._btn_select_splits_profile.clicked.connect(self._btn_select_splits_profile_on_click)
        #self._btn_settings.clicked.connect(self._btn_settings_on_click)
        #self._btn_pause.clicked.connect(self._worker_on_pause_status_updated)
        #self._btn_start_stop.clicked.connect(self._btn_start_stop_on_click)

        # screen watch worker
        self._workerThread: Optional[QThread] = None
        #self._worker: Optional[ScreenWatchWorker] = None

    #########################
    # Construct sub-layouts #
    #########################

    def _construct_main_layout(self) -> QHBoxLayout:
        self._lbl_worker_status = QLabel("Waiting for you to start\nthe screen watch worker.")
        self._lbl_detailed_status = QLabel("-")

        main_layout: QHBoxLayout = QHBoxLayout()
        main_layout.addWidget(self._lbl_worker_status)
        main_layout.addWidget(self._lbl_detailed_status)

        return main_layout

    def _construct_splits_profiles_layout(self) -> QHBoxLayout:
        self._lbl_current_splits_profile: QLabel = QLabel()
        self._btn_select_splits_profile: QPushButton = QPushButton("Select Splits Profile")

        splits_profiles_layout: QHBoxLayout = QHBoxLayout()
        splits_profiles_layout.addWidget(self._lbl_current_splits_profile)
        splits_profiles_layout.addWidget(self._btn_select_splits_profile)

        return splits_profiles_layout

    def _construct_buttons_layout(self) -> QHBoxLayout:
        self._btn_settings = QPushButton("Settings")
        self._btn_pause = QPushButton("Pause")
        self._btn_start_stop = QPushButton("Start")

        buttons_layout: QHBoxLayout = QHBoxLayout()
        buttons_layout.addWidget(self._btn_settings)
        buttons_layout.addWidget(self._btn_pause)
        buttons_layout.addWidget(self._btn_start_stop)

        return buttons_layout

    ########################
    # Button functionality #
    ########################
