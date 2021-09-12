from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QThread
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

from src import Config
from src import SplitsProfile
from src.ScreenWatchWorker import ScreenWatchWorker
from src.SetupWidget import SetupWidget
from src.SplitsProfileSelectorDialog import SplitsProfileSelectorDialog


class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._workerThread: Optional[QThread] = None
        self._worker: Optional[ScreenWatchWorker] = None

        self.setWindowTitle("Blackscreen Autosplitter")

        self.layout = QVBoxLayout(self)

        main_layout = QHBoxLayout()
        self._lbl_worker_status = QLabel("Waiting for you to start\nthe screen watch worker.")
        main_layout.addWidget(self._lbl_worker_status)

        self._lbl_detailed_status = QLabel("-")
        main_layout.addWidget(self._lbl_detailed_status)
        self.layout.addLayout(main_layout)

        splits_profiles_layout = QHBoxLayout()
        self._lbl_current_splits_profile: QLabel = QLabel()
        self._update_lbl_current_splits_profile()
        splits_profiles_layout.addWidget(self._lbl_current_splits_profile)

        self._btn_select_splits_profile: QPushButton = QPushButton("Select Splits Profile")
        self._btn_select_splits_profile.clicked.connect(self._btn_select_splits_profile_on_click)
        splits_profiles_layout.addWidget(self._btn_select_splits_profile)
        self.layout.addLayout(splits_profiles_layout)

        buttons_layout = QHBoxLayout()
        self._btn_settings = QPushButton("Settings")
        self._btn_settings.clicked.connect(self._btn_settings_on_click)
        buttons_layout.addWidget(self._btn_settings)

        self._btn_pause = QPushButton("Pause")
        self._btn_pause.clicked.connect(self._worker_on_pause_status_updated)
        buttons_layout.addWidget(self._btn_pause)

        self._btn_start_stop = QPushButton("Start")
        self._btn_start_stop.clicked.connect(self._btn_start_stop_on_click)
        buttons_layout.addWidget(self._btn_start_stop)
        self.layout.addLayout(buttons_layout)

    def _update_lbl_current_splits_profile(self):
        splits_profile_text = "Current Splits Profile: "
        if Config.path_to_current_splits_profile == "":
            splits_profile_text += "-"
        else:
            splits_profile_text += SplitsProfile.load_from_file(Config.path_to_current_splits_profile).name
        self._lbl_current_splits_profile.setText(splits_profile_text)

    def _worker_on_blackscreen_counter_updated(self, blackscreen_counter: int):
        if self._worker is None:
            self._lbl_detailed_status.setText("-")
            return

        # figure out blackscreen count of next split
        next_split_index = blackscreen_counter + 1
        final_split_index = max(self._worker.get_splits_profile().get_split_indices())
        while (next_split_index <= final_split_index) and (next_split_index not in self._worker.get_splits_profile().splits):
            next_split_index += 1

        s: str = "Blackscreen Counter: " + str(blackscreen_counter)
        s += "\n"
        s += "Next Split: " + str(min(next_split_index, final_split_index))
        s += " - "
        s += self._worker.get_splits_profile().name_of_split(min(next_split_index, final_split_index))
        self._lbl_detailed_status.setText(s)

    def _worker_on_pause_status_updated(self):
        if self._worker is None:
            return

        if self._worker.is_paused():
            self._worker.unpause()
            self._btn_pause.setText("Pause")
            self._lbl_worker_status.setStyleSheet("QLabel { color:green; }")
            self._lbl_worker_status.setText(
                "Worker running with profile\n" + self._worker.get_splits_profile().name + ".")
        else:
            self._worker.pause()
            self._btn_pause.setText("Unpause")
            self._lbl_worker_status.setStyleSheet("QLabel { color:orange; }")
            self._lbl_worker_status.setText(
                "Worker paused with profile\n" + self._worker.get_splits_profile().name + ".")

    def _btn_select_splits_profile_on_click(self):
        splits_profile_selector_dialog = SplitsProfileSelectorDialog()
        splits_profile_selector_dialog.exec()
        self._update_lbl_current_splits_profile()

    def _btn_settings_on_click(self):
        self._open_settings()

    def _open_settings(self):
        self._setup_widget = SetupWidget()
        self._setup_widget.show()

    def _btn_start_stop_on_click(self):
        # if worker is not started start it, otherwise stop it
        if self._worker is None:
            self._start_worker()
        else:
            self._stop_worker()

    def _start_worker(self):
        if Config.path_to_current_splits_profile == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("You first have to select a splits profile before you can start the splitter!")
            msg.exec()
            return

        self._btn_select_splits_profile.setEnabled(False)
        self._btn_start_stop.setText("Stop")

        self._workerThread = QtCore.QThread()
        self._worker = ScreenWatchWorker(SplitsProfile.load_from_file(Config.path_to_current_splits_profile))
        self._worker.moveToThread(self._workerThread)
        self._workerThread.started.connect(self._worker.run)
        self._workerThread.start()

        self._lbl_worker_status.setStyleSheet("QLabel { color:green; }")
        self._lbl_worker_status.setText("Worker running with profile\n" + self._worker.get_splits_profile().name + ".")

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

    def closeEvent(self, event: QCloseEvent):
        self._stop_worker()
