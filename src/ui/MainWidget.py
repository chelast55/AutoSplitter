from typing import Optional
from PySide6 import QtCore
from PySide6.QtCore import QThread
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from pathlib import Path

from src import config
from src.ScreenWatchWorker import ScreenWatchWorker
from src.ui.SettingsWidget import SettingsWidget
from src.ui.SplitsProfileSelectorDialog import SplitsProfileSelectorDialog


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
        self._update_lbl_current_splits_profile()

        # connect functionality to buttons
        self._btn_select_splits_profile.clicked.connect(self._btn_select_splits_profile_on_click)
        self._btn_settings.clicked.connect(self._btn_settings_on_click)
        self._btn_pause.clicked.connect(self._worker_on_pause_status_updated)
        self._btn_start_stop.clicked.connect(self._btn_start_stop_on_click)

        # screen watch worker
        self._workerThread: Optional[QThread] = None
        self._worker: Optional[ScreenWatchWorker] = None

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

    ################
    # Misc. visual #
    ################

    def _update_lbl_current_splits_profile(self):
        splits_profile_text: str = "Splits Profile: "
        if config.get_current_splits_profile_path() == Path(""):
            splits_profile_text += "-"
        else:
            splits_profile_text += '\"' + config.get_current_splits_profile().get_name() + '\"'
        self._lbl_current_splits_profile.setText(splits_profile_text)

    ########################
    # Button functionality #
    ########################

    def _btn_select_splits_profile_on_click(self):
        splits_profile_selector_dialog: SplitsProfileSelectorDialog = SplitsProfileSelectorDialog()
        splits_profile_selector_dialog.exec()
        self._update_lbl_current_splits_profile()

    def _btn_settings_on_click(self):
        self._setup_widget = SettingsWidget()
        self._setup_widget.show()

    def _btn_start_stop_on_click(self):
        # if worker is not started, start it, otherwise stop it
        if self._worker is None:
            self._start_worker()
        else:
            self._stop_worker()

    ########################
    # Worker functionality #
    ########################

    def _start_worker(self):
        if config.get_current_splits_profile_path() == Path(""):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("You first have to select a splits profile before you can start the splitter!")
            msg.exec()
            return

        self._btn_select_splits_profile.setEnabled(False)
        self._btn_start_stop.setText("Stop")

        self._workerThread = QtCore.QThread()
        self._worker = ScreenWatchWorker(config.get_current_splits_profile())
        self._worker.moveToThread(self._workerThread)
        self._workerThread.started.connect(self._worker.run)
        self._workerThread.start()

        self._lbl_worker_status.setStyleSheet("QLabel { color:green; }")
        self._lbl_worker_status.setText(f"Worker running with profile\n{self._worker.get_splits_profile().get_name()}.")

        self._worker.blackscreen_counter_updated.connect(self._worker_on_blackscreen_counter_updated)
        self._worker_on_blackscreen_counter_updated(0)
        self._worker.pause_status_updated.connect(self._worker_on_pause_status_updated)

    def _stop_worker(self):
        self._btn_select_splits_profile.setEnabled(True)
        self._btn_start_stop.setText("Start")

        if self._worker is not None:
            self._worker.finish()
        self._worker = None

        if self._workerThread is not None:
            self._workerThread.quit()
            self._workerThread.wait()
        self._workerThread = None

        self._lbl_detailed_status.setText("-")

        self._lbl_worker_status.setStyleSheet("QLabel { color:red; }")
        self._lbl_worker_status.setText("Worker stopped.")
        self._btn_pause.setText("Pause")

    def _worker_on_blackscreen_counter_updated(self, blackscreen_counter: int):
        if self._worker is None:
            self._lbl_detailed_status.setText("-")
            return

        # figure out blackscreen count of next split
        next_split_index = blackscreen_counter + 1
        final_split_index = max(self._worker.get_splits_profile().get_split_indices())
        while (next_split_index <= final_split_index) and (
                next_split_index not in self._worker.get_splits_profile().get_splits()):
            next_split_index += 1

        s: str = (f"Blackscreen Counter: {blackscreen_counter}\n"
                  f"Next Split: {min(next_split_index, final_split_index)} - "
                  f"{self._worker.get_splits_profile().get_splits().get(min(next_split_index, final_split_index))}")
        self._lbl_detailed_status.setText(s)

    def _worker_on_pause_status_updated(self):
        if self._worker is None:
            return

        if self._worker.is_paused():
            self._worker.unpause()
            self._btn_pause.setText("Pause")
            self._lbl_worker_status.setStyleSheet("QLabel { color:green; }")
            self._lbl_worker_status.setText(
                "Worker running with profile\n" + self._worker.get_splits_profile().get_name() + ".")
        else:
            self._worker.pause()
            self._btn_pause.setText("Unpause")
            self._lbl_worker_status.setStyleSheet("QLabel { color:orange; }")
            self._lbl_worker_status.setText(
                "Worker paused with profile\n" + self._worker.get_splits_profile().get_name() + ".")

    def closeEvent(self, event: QCloseEvent):
        self._stop_worker()
