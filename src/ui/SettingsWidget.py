"""(GUI) Graphical Settings Menu for setting coordinates for area to observe and various other config parameters"""

import math
import os
from PIL.Image import Image
from PySide6.QtCore import Qt, QTimer, QThread
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QDialogButtonBox, QSpinBox, QLabel, \
    QCheckBox, QPushButton, QGroupBox, QDoubleSpinBox

from src import config
from src.ui.KeyPickerWidget import KeyPickerWidget
#from src.ui.QRectSelectGraphicsView import QRectSelectGraphicsView
#from src.ui.SettingsVideoPreviewWorker import SettingsVideoPreviewWorker


# TODO: Allow to somehow change between setting something globally and on a splits profile basis
from src.ui.TupleHBoxLayout import TupleHBoxLayout


class SettingsWidget(QWidget):

    def __init__(self):
        super(SettingsWidget, self).__init__()

        self.setAttribute(Qt.WA_AlwaysShowToolTips, True)

        self.setWindowTitle("Settings")
        self.resize(1400, 700)

        self._global_options_mode_enabled: bool = True
        """
        True: Global settings change when edited\n
        False: Override of changed settings for current splits profile is created
        """

        self._tmr_preview_image: QTimer = QTimer(self)
        self._tmr_preview_image.setInterval(200)
        self._video_preview_thread: QThread = QThread()
        #self._video_preview_worker: SettingsVideoPreviewWorker = SettingsVideoPreviewWorker()
        #self._video_preview_worker.moveToThread(self._video_preview_thread)
        self._tmr_preview_image.moveToThread(self._video_preview_thread)
        #self._tmr_preview_image.timeout.connect(self._video_preview_worker.run)
        #self._video_preview_thread.started.connect(self._tmr_preview_image.start)
        #self._video_preview_worker.gray_value_updated.connect(self._preview_on_gray_value_updated)
        #self._video_preview_worker.image_captured.connect(self._preview_on_image_captured)
        self._video_preview_thread.start()
        self._tmr_info: QTimer = QTimer(self)
        self._tmr_info.setInterval(200)
        #self._tmr_info.timeout.connect(self._on_info_timeout)
        self._tmr_info.start()

        #self._gv_preview_image: QRectSelectGraphicsView = QRectSelectGraphicsView()
        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._btn_change_options_mode: QPushButton = QPushButton("Edit Per-Profile Settings")
        self._btn_restore_defaults: QPushButton = QPushButton("Restore Default Settings")
        self._lbl_options_mode_status: QLabel = QLabel("Global settings:")
        self._lbl_split: QLabel = QLabel("Split Key:")
        self._key_picker_split: KeyPickerWidget = KeyPickerWidget()
        self._lbl_pause: QLabel = QLabel("Pause Key:")
        self._key_picker_pause: KeyPickerWidget = KeyPickerWidget()
        self._lbl_reset: QLabel = QLabel("Reset Key:")
        self._key_picker_reset: KeyPickerWidget = KeyPickerWidget()
        self._lbl_decrement: QLabel = QLabel("Decrement Key:")
        self._key_picker_decrement: KeyPickerWidget = KeyPickerWidget()
        self._lbl_increment: QLabel = QLabel("Increment Key:")
        self._key_picker_increment: KeyPickerWidget = KeyPickerWidget()
        self._lbl_blackscreen_threshold: QLabel = QLabel("Blackscreen Threshold (0-255):")
        self._sb_blackscreen_threshold: QSpinBox = QSpinBox()
        self._sb_blackscreen_threshold.setMinimum(0)
        self._sb_blackscreen_threshold.setMaximum(255)
        self._sb_blackscreen_threshold_override: QSpinBox = QSpinBox()
        self._sb_blackscreen_threshold_override.setMinimum(0)
        self._sb_blackscreen_threshold_override.setMaximum(255)
        self._btn_automatic_threshold: QPushButton = QPushButton("Start Automatic Threshold Detection")
        self._btn_automatic_threshold.setCheckable(True)
        self._lbl_after_split_delay: QLabel = QLabel("After Split Delay (s):")
        self._dsb_after_split_delay: QDoubleSpinBox = QDoubleSpinBox()
        self._dsb_after_split_delay.setDecimals(2)
        self._dsb_after_split_delay.setMinimum(0)
        self._dsb_after_split_delay.setMaximum(999)
        self._dsb_after_split_delay_override: QDoubleSpinBox = QDoubleSpinBox()
        self._dsb_after_split_delay_override.setDecimals(2)
        self._dsb_after_split_delay_override.setMinimum(0)
        self._dsb_after_split_delay_override.setMaximum(999)
        self._lbl_advanced_settings: QLabel = QLabel("Show Advanced Settings")
        self._cb_advanced_settings: QCheckBox = QCheckBox()
        self._lbl_max_capture_rate: QLabel = QLabel()
        self._sb_max_capture_rate: QSpinBox = QSpinBox()
        self._sb_max_capture_rate.setMinimum(1)
        self._sb_max_capture_rate.setMaximum(999)
        self._sb_max_capture_rate_override: QSpinBox = QSpinBox()
        self._sb_max_capture_rate_override.setMinimum(1)
        self._sb_max_capture_rate_override.setMaximum(999)
        self._lbl_after_key_press_delay: QLabel = QLabel()
        self._dsb_after_key_press_delay: QDoubleSpinBox = QDoubleSpinBox()
        self._dsb_after_key_press_delay.setDecimals(2)
        self._dsb_after_key_press_delay.setMinimum(0)
        self._dsb_after_key_press_delay.setMaximum(999)
        self._dsb_after_key_press_delay_override: QDoubleSpinBox = QDoubleSpinBox()
        self._dsb_after_key_press_delay_override.setDecimals(2)
        self._dsb_after_key_press_delay_override.setMinimum(0)
        self._dsb_after_key_press_delay_override.setMaximum(999)
        self._lbl_automatic_threshold_overhead: QLabel = QLabel()
        self._sb_automatic_threshold_overhead: QSpinBox = QSpinBox()
        self._sb_automatic_threshold_overhead.setMinimum(0)
        self._sb_automatic_threshold_overhead.setMaximum(255)
        self._sb_automatic_threshold_overhead_override: QSpinBox = QSpinBox()
        self._sb_automatic_threshold_overhead_override.setMinimum(0)
        self._sb_automatic_threshold_overhead_override.setMaximum(255)
        self._lbl_info: QLabel = QLabel()
        self._lbl_info.setWordWrap(True)
        self._info_box: QVBoxLayout = QVBoxLayout()
        self._gb_info_highlight: QGroupBox = QGroupBox("Info:")
        self._gb_info_highlight.setLayout(self._info_box)
        self._info_box.addWidget(self._lbl_info)

        self._key_picker_split.set_key(config.get_split_key())
        self._key_picker_pause.set_key(config.get_pause_key())
        self._key_picker_reset.set_key(config.get_reset_key())
        self._key_picker_decrement.set_key(config.get_decrement_key())
        self._key_picker_increment.set_key(config.get_increment_key())
        self._sb_blackscreen_threshold.setValue(config.get_blackscreen_threshold())
        self._dsb_after_split_delay.setValue(config.get_after_split_delay())
        self._lbl_max_capture_rate.setText("Max Capture Rate (1/s):")
        self._sb_max_capture_rate.setValue(config.get_max_capture_rate())
        self._lbl_after_key_press_delay.setText("After Key Press Delay (s):")
        self._dsb_after_key_press_delay.setValue(config.get_after_key_press_delay())
        self._lbl_automatic_threshold_overhead.setText("Automatic Threshold Overhead (0-255):")
        self._sb_automatic_threshold_overhead.setValue(config.get_automatic_threshold_overhead())

        #if len(config.get_video_preview_coords()) == 4:
            #self._gv_preview_image.set_rect(config.get_video_preview_coords()[0],
            #                                config.get_video_preview_coords()[1],
            #                                config.get_video_preview_coords()[2],
            #                                config.get_video_preview_coords()[3])

        self.setWindowModality(Qt.ApplicationModal)
        self.layout = QVBoxLayout(self)

        if config.get_current_splits_profile_path() == "":
            self._btn_change_options_mode.setEnabled(False)

        settings_layout = QHBoxLayout()

        settings_and_info_layout = QVBoxLayout()
        settings_and_info_layout.addWidget(self._btn_change_options_mode)
        settings_and_info_layout.addWidget(self._btn_restore_defaults)
        settings_and_info_layout.addWidget(self._lbl_options_mode_status)
        button_settings_layout = QFormLayout()
        button_settings_layout.addRow(self._lbl_split, self._key_picker_split)
        button_settings_layout.addRow(self._lbl_pause, self._key_picker_pause)
        button_settings_layout.addRow(self._lbl_reset, self._key_picker_reset)
        button_settings_layout.addRow(self._lbl_decrement, self._key_picker_decrement)
        button_settings_layout.addRow(self._lbl_increment, self._key_picker_increment)
        row_blackscreen_threshold = QHBoxLayout()
        row_blackscreen_threshold.addWidget(self._sb_blackscreen_threshold)
        row_blackscreen_threshold.addWidget(self._sb_blackscreen_threshold_override)
        button_settings_layout.addRow(self._lbl_blackscreen_threshold,
                                      TupleHBoxLayout(self._sb_blackscreen_threshold,
                                                      self._sb_blackscreen_threshold_override))
        button_settings_layout.addWidget(self._btn_automatic_threshold)
        button_settings_layout.addRow(self._lbl_after_split_delay,
                                      TupleHBoxLayout(self._dsb_after_split_delay,
                                                      self._dsb_after_split_delay_override))
        button_settings_layout.addRow(self._lbl_advanced_settings, self._cb_advanced_settings)
        button_settings_layout.addRow(self._lbl_max_capture_rate,
                                      TupleHBoxLayout(self._sb_max_capture_rate,
                                                      self._sb_max_capture_rate_override))
        button_settings_layout.addRow(self._lbl_after_key_press_delay,
                                      TupleHBoxLayout(self._dsb_after_key_press_delay,
                                                      self._dsb_after_key_press_delay_override))
        button_settings_layout.addRow(self._lbl_automatic_threshold_overhead,
                                      TupleHBoxLayout(self._sb_automatic_threshold_overhead,
                                                      self._sb_automatic_threshold_overhead_override))
        settings_and_info_layout.addLayout(button_settings_layout)
        settings_and_info_layout.addStretch()
        settings_and_info_layout.addWidget(self._gb_info_highlight)
        settings_layout.addLayout(settings_and_info_layout)

        # hide advanced settings initially
        self._lbl_max_capture_rate.setVisible(False)
        self._sb_max_capture_rate.setVisible(False)
        self._sb_max_capture_rate_override.setVisible(False)
        self._lbl_after_key_press_delay.setVisible(False)
        self._dsb_after_key_press_delay.setVisible(False)
        self._dsb_after_key_press_delay_override.setVisible(False)
        self._lbl_automatic_threshold_overhead.setVisible(False)
        self._sb_automatic_threshold_overhead.setVisible(False)
        self._sb_automatic_threshold_overhead_override.setVisible(False)

        # disable and hide all override spin boxes initially
        self._sb_blackscreen_threshold_override.setEnabled(False)
        self._sb_blackscreen_threshold_override.setVisible(False)
        self._dsb_after_split_delay_override.setEnabled(False)
        self._dsb_after_split_delay_override.setVisible(False)
        self._sb_max_capture_rate_override.setEnabled(False)
        self._dsb_after_key_press_delay_override.setEnabled(False)
        self._sb_automatic_threshold_overhead_override.setEnabled(False)

        rect_select_layout: QVBoxLayout = QVBoxLayout()
        rect_select_layout.addWidget(QLabel("Drag on the preview image to select the region "
                                            "of the screen that should be checked for blackscreens."))
        #rect_select_layout.addWidget(self._gv_preview_image)
        self._lbl_gray_value: QLabel = QLabel("Avg. Gray Value: -")
        rect_select_layout.addWidget(self._lbl_gray_value)
        settings_layout.addLayout(rect_select_layout)

        self.layout.addLayout(settings_layout)

        #self._btn_change_options_mode.clicked.connect(self._btn_switch_options_mode_on_click)
        #self._btn_restore_defaults.clicked.connect(self._btn_restore_defaults_on_click)
        #self._btn_automatic_threshold.toggled.connect(self._btn_automatic_threshold_on_toggle)
        #self._cb_advanced_settings.stateChanged.connect(self._cb_advanced_settings_state_changed)

        #self._btn_box.accepted.connect(self._btn_box_accepted)
        #self._btn_box.rejected.connect(self._btn_box_rejected)
        self.layout.addWidget(self._btn_box)
