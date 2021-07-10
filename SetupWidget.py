import math

from PIL import ImageGrab
from PIL.Image import Image
from PySide6.QtCore import Qt, QTimer, QThread
from PySide6.QtGui import QPixmap, QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QDialogButtonBox, QSpinBox, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem, QLabel, QCheckBox, QPushButton

import Config
import ImageAnalyzer
from KeyPickerWidget import KeyPickerWidget
from QRectSelectGraphicsView import QRectSelectGraphicsView
from SettingsVideoPreviewWorker import SettingsVideoPreviewWorker


class SetupWidget(QWidget):

    def __init__(self):
        super(SetupWidget, self).__init__()
        self.setAttribute(Qt.WA_AlwaysShowToolTips, True)

        self.setWindowTitle("Settings")
        self.resize(1400, 600)

        self._tmr_preview_image: QTimer = QTimer(self)
        self._tmr_preview_image.setInterval(200)
        self._video_preview_thread: QThread = QThread()
        self._video_preview_worker: SettingsVideoPreviewWorker = SettingsVideoPreviewWorker()
        self._video_preview_worker.moveToThread(self._video_preview_thread)
        self._tmr_preview_image.moveToThread(self._video_preview_thread)
        self._tmr_preview_image.timeout.connect(self._video_preview_worker.run)
        self._video_preview_thread.started.connect(self._tmr_preview_image.start)
        self._video_preview_worker.gray_value_updated.connect(self._preview_on_gray_value_updated)
        self._video_preview_worker.image_captured.connect(self._preview_on_image_captured)
        self._video_preview_thread.start()

        self._gv_preview_image: QRectSelectGraphicsView = QRectSelectGraphicsView()
        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._key_picker_split: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_pause: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_reset: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_decrement: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_increment: KeyPickerWidget = KeyPickerWidget()
        self._sb_blackscreen_threshold: QSpinBox = QSpinBox()
        self._btn_automatic_threshold: QPushButton = QPushButton("Start Automatic Threshold Detection")
        self._btn_automatic_threshold.setCheckable(True)
        self._sb_blackscreen_threshold.setMinimum(0.0)
        self._sb_blackscreen_threshold.setMaximum(255.0)
        self._sb_after_split_delay: QSpinBox = QSpinBox()
        self._sb_after_split_delay.setMinimum(0)
        self._sb_after_split_delay.setMaximum(999)
        self._cb_advanced_settings: QCheckBox = QCheckBox()
        self._lbl_max_capture_rate: QLabel = QLabel()
        self._sb_max_capture_rate: QSpinBox = QSpinBox()
        self._sb_max_capture_rate.setMinimum(1)
        self._sb_max_capture_rate.setMaximum(999)
        self._lbl_after_key_press_delay: QLabel = QLabel()
        self._sb_after_key_press_delay: QSpinBox = QSpinBox()
        self._sb_after_key_press_delay.setMinimum(0)
        self._sb_after_key_press_delay.setMaximum(999)
        self._lbl_automatic_threshold_overhead: QLabel = QLabel()
        self._sb_automatic_threshold_overhead: QSpinBox = QSpinBox()
        self._sb_automatic_threshold_overhead.setMinimum(0)
        self._sb_automatic_threshold_overhead.setMaximum(999)

        self._key_picker_split.set_key(Config.split_key)
        self._key_picker_pause.set_key(Config.pause_key)
        self._key_picker_reset.set_key(Config.reset_key)
        self._key_picker_decrement.set_key(Config.decrement_key)
        self._key_picker_increment.set_key(Config.increment_key)
        self._sb_blackscreen_threshold.setValue(Config.blackscreen_threshold)
        self._sb_after_split_delay.setValue(Config.after_split_delay)
        self._lbl_max_capture_rate.setText("Max Capture Rate (1/s):")
        self._sb_max_capture_rate.setValue(Config.max_capture_rate)
        self._lbl_after_key_press_delay.setText("After Key Press Delay (s):")
        self._sb_after_split_delay.setValue(Config.after_split_delay)
        self._lbl_automatic_threshold_overhead.setText("Automatic Threshold Overhead (s):")
        self._sb_automatic_threshold_overhead.setValue(Config.automatic_threshold_overhead)
        self._gv_preview_image.set_rect(Config.video_preview_coords[0],
                                        Config.video_preview_coords[1],
                                        Config.video_preview_coords[2],
                                        Config.video_preview_coords[3])

        self._key_picker_split.setToolTip("Key automatically pressed when a blackscreen is detected")
        self._key_picker_pause.setToolTip("Key to pause/unpause the blackscreen detection")
        self._key_picker_reset.setToolTip("Key to reset the blackscreen counter")
        self._key_picker_decrement.setToolTip("Key to subtract 1 from the blackscreen counter")
        self._key_picker_increment.setToolTip("Key to add 1 to the blackscreen counter")
        self._sb_blackscreen_threshold.setToolTip("Maximum Avg. Gray Value the selected area can have to still be considered a \"blackscreen\"")
        self._sb_after_split_delay.setToolTip("Delay after a blackscreen was successfully detected to prevent multiple splits per blackscreen")
        self._cb_advanced_settings.setToolTip("The default values for these should work in most cases")
        self._sb_max_capture_rate.setToolTip("Times/second a capture is taken (NOTE: this is a maximum and possibly unreachable)")
        self._sb_after_key_press_delay.setToolTip("Delay after any key press to prevent multiple registrations")
        self._sb_automatic_threshold_overhead.setToolTip("Value added to automatically calculated threshold for better tolerance")

        self.setWindowModality(Qt.ApplicationModal)
        self.layout = QVBoxLayout(self)

        settings_layout = QHBoxLayout()

        button_settings_layout = QFormLayout()
        button_settings_layout.addRow("Split Key:", self._key_picker_split)
        button_settings_layout.addRow("Pause Key:", self._key_picker_pause)
        button_settings_layout.addRow("Reset Key:", self._key_picker_reset)
        button_settings_layout.addRow("Decrement Key:", self._key_picker_decrement)
        button_settings_layout.addRow("Increment Key:", self._key_picker_increment)
        button_settings_layout.addRow("Blackscreen Threshold (0-255):", self._sb_blackscreen_threshold)
        button_settings_layout.addWidget(self._btn_automatic_threshold)
        button_settings_layout.addRow("After Split Delay (s):", self._sb_after_split_delay)
        button_settings_layout.addRow("Show Advanced Settings", self._cb_advanced_settings)
        button_settings_layout.addRow(self._lbl_max_capture_rate, self._sb_max_capture_rate)
        button_settings_layout.addRow(self._lbl_after_key_press_delay, self._sb_after_key_press_delay)
        button_settings_layout.addRow(self._lbl_automatic_threshold_overhead, self._sb_automatic_threshold_overhead)
        settings_layout.addLayout(button_settings_layout)

        self._lbl_max_capture_rate.setVisible(False)
        self._sb_max_capture_rate.setVisible(False)
        self._lbl_after_key_press_delay.setVisible(False)
        self._sb_after_key_press_delay.setVisible(False)
        self._lbl_automatic_threshold_overhead.setVisible(False)
        self._sb_automatic_threshold_overhead.setVisible(False)

        rect_select_layout: QVBoxLayout = QVBoxLayout()
        rect_select_layout.addWidget(QLabel("Drag on the preview image to select the region "
                                            "of the screen that should be checked for blackscreens."))
        rect_select_layout.addWidget(self._gv_preview_image)
        self._lbl_gray_value: QLabel = QLabel("Avg. Gray Value: -")
        rect_select_layout.addWidget(self._lbl_gray_value)
        settings_layout.addLayout(rect_select_layout)

        self.layout.addLayout(settings_layout)

        self._btn_automatic_threshold.toggled.connect(self._btn_automatic_threshold_on_toggle)
        self._cb_advanced_settings.stateChanged.connect(self._cb_advanced_settings_state_changed)

        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)
        self.layout.addWidget(self._btn_box)

    def _preview_on_gray_value_updated(self, gray_value: float):
        if self._gv_preview_image.has_area():
            self._lbl_gray_value.setText("Avg. Gray Value: " + str(gray_value))
            if self._btn_automatic_threshold.isChecked():
                new_gray_threshold = math.ceil(gray_value + Config.automatic_threshold_overhead)
                if new_gray_threshold < self._sb_blackscreen_threshold.value():
                    self._sb_blackscreen_threshold.setValue(new_gray_threshold)

    def _preview_on_image_captured(self, img: Image):
        self._gv_preview_image.set_image(img)

    def _btn_automatic_threshold_on_toggle(self):
        if self._btn_automatic_threshold.isChecked():
            self._btn_automatic_threshold.setText("Stop Automatic Threshold Detection")
            self._btn_box.button(QDialogButtonBox.Ok).setEnabled(False)
            self._sb_blackscreen_threshold.setValue(255)
        else:
            self._btn_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self._btn_automatic_threshold.setText("Start Automatic Threshold Detection")

    def _cb_advanced_settings_state_changed(self):
        self._lbl_max_capture_rate.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_max_capture_rate.setVisible(self._cb_advanced_settings.isChecked())
        self._lbl_after_key_press_delay.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_after_key_press_delay.setVisible(self._cb_advanced_settings.isChecked())
        self._lbl_automatic_threshold_overhead.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_automatic_threshold_overhead.setVisible(self._cb_advanced_settings.isChecked())

    def _btn_box_accepted(self):
        Config.split_key = self._key_picker_split.key
        Config.pause_key = self._key_picker_pause.key
        Config.reset_key = self._key_picker_reset.key
        Config.decrement_key = self._key_picker_decrement.key
        Config.increment_key = self._key_picker_increment.key
        Config.blackscreen_threshold = self._sb_blackscreen_threshold.value()
        Config.after_split_delay = self._sb_after_split_delay.value()
        Config.video_preview_coords = self._gv_preview_image.get_rect()
        Config.max_capture_rate = self._sb_max_capture_rate.value()
        Config.after_key_press_delay = self._sb_after_key_press_delay.value()
        Config.automatic_threshold_overhead = self._sb_automatic_threshold_overhead.value()
        Config.write_config_to_file()
        self.close()

    def _btn_box_rejected(self):
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._tmr_preview_image.stop()
