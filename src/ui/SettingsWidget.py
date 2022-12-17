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
from src.ui.RectSelectGraphicsView import RectSelectGraphicsView
# from src.ui.SettingsVideoPreviewWorker import SettingsVideoPreviewWorker


# TODO: Allow to somehow change between setting something globally and on a splits profile basis
from src.ui.TupleHBoxLayout import TupleHBoxLayout


class SettingsWidget(QWidget):

    def __init__(self):
        super(SettingsWidget, self).__init__()

        self._global_options_mode_enabled: bool = True
        """
        True: Global settings change when edited\n
        False: Override of changed settings for current splits profile is created
        """

        # Window Setup
        self.setWindowTitle("Settings")
        self.resize(1400, 700)
        self.setAttribute(Qt.WA_AlwaysShowToolTips, True)
        self.setWindowModality(Qt.ApplicationModal)

        # Layout
        self._construct_top_elements()
        _button_settings_layout: QFormLayout = self._construct_button_settings_layout()
        self._construct_info_elements()
        _rect_select_layout: QVBoxLayout = self._construct_rect_select_layout()
        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        _settings_and_info_layout: QVBoxLayout = QVBoxLayout()
        _settings_and_info_layout.addWidget(self._btn_change_options_mode)
        _settings_and_info_layout.addWidget(self._btn_restore_defaults)
        _settings_and_info_layout.addWidget(self._lbl_options_mode_status)
        _settings_and_info_layout.addLayout(_button_settings_layout)
        _settings_and_info_layout.addStretch()
        _settings_and_info_layout.addWidget(self._gb_info_highlight)

        _settings_layout: QHBoxLayout = QHBoxLayout()
        _settings_layout.addLayout(_settings_and_info_layout)
        _settings_layout.addLayout(_rect_select_layout)

        self._layout = QVBoxLayout(self)
        self._layout.addLayout(_settings_layout)
        self._layout.addWidget(self._btn_box)

        # misc. visual setup
        self._hide_advanced_settings()
        self._disable_override_spin_boxes()
        self._load_from_config()

        # Background tasks
        self._init_video_preview_thread()
        self._init_info_timer()

        # connect functionality to buttons
        # self._btn_change_options_mode.clicked.connect(self._btn_switch_options_mode_on_click)
        # self._btn_restore_defaults.clicked.connect(self._btn_restore_defaults_on_click)
        # self._btn_automatic_threshold.toggled.connect(self._btn_automatic_threshold_on_toggle)
        self._cb_advanced_settings.stateChanged.connect(self._cb_advanced_settings_state_changed)
        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)

    #########################
    # Construct sub-layouts #
    #########################

    def _construct_top_elements(self) -> None:
        self._btn_change_options_mode: QPushButton = QPushButton("Edit Per-Profile Settings")
        self._btn_restore_defaults: QPushButton = QPushButton("Restore Default Settings")
        self._lbl_options_mode_status: QLabel = QLabel("Global settings:")

    def _construct_button_settings_layout(self) -> QFormLayout:
        # Initialize
        self._lbl_split: QLabel = QLabel("Split Key:")
        self._lbl_pause: QLabel = QLabel("Pause Key:")
        self._lbl_reset: QLabel = QLabel("Reset Key:")
        self._lbl_decrement: QLabel = QLabel("Decrement Key:")
        self._lbl_increment: QLabel = QLabel("Increment Key:")
        self._lbl_blackscreen_threshold: QLabel = QLabel("Blackscreen Threshold (0-255):")
        self._key_picker_split: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_pause: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_reset: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_decrement: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_increment: KeyPickerWidget = KeyPickerWidget()
        self._sb_blackscreen_threshold: QSpinBox = QSpinBox()
        self._sb_blackscreen_threshold_override: QSpinBox = QSpinBox()
        self._btn_automatic_threshold: QPushButton = QPushButton("Start Automatic Threshold Detection")
        self._lbl_after_split_delay: QLabel = QLabel("After Split Delay (s):")
        self._dsb_after_split_delay: QDoubleSpinBox = QDoubleSpinBox()
        self._dsb_after_split_delay_override: QDoubleSpinBox = QDoubleSpinBox()
        self._lbl_advanced_settings: QLabel = QLabel("Show Advanced Settings")
        self._cb_advanced_settings: QCheckBox = QCheckBox()
        self._lbl_max_capture_rate: QLabel = QLabel("Max Capture Rate (1/s):")
        self._sb_max_capture_rate: QSpinBox = QSpinBox()
        self._sb_max_capture_rate_override: QSpinBox = QSpinBox()
        self._lbl_after_key_press_delay: QLabel = QLabel("After Key Press Delay (s):")
        self._dsb_after_key_press_delay: QDoubleSpinBox = QDoubleSpinBox()
        self._dsb_after_key_press_delay_override: QDoubleSpinBox = QDoubleSpinBox()
        self._lbl_automatic_threshold_overhead: QLabel = QLabel("Automatic Threshold Overhead (0-255):")
        self._sb_automatic_threshold_overhead: QSpinBox = QSpinBox()
        self._sb_automatic_threshold_overhead_override: QSpinBox = QSpinBox()

        # Setup
        self._sb_blackscreen_threshold.setMinimum(0)
        self._sb_blackscreen_threshold.setMaximum(255)
        self._sb_blackscreen_threshold_override.setMinimum(0)
        self._sb_blackscreen_threshold_override.setMaximum(255)
        self._btn_automatic_threshold.setCheckable(True)
        self._dsb_after_split_delay.setDecimals(2)
        self._dsb_after_split_delay.setMinimum(0)
        self._dsb_after_split_delay.setMaximum(999)
        self._dsb_after_split_delay_override.setDecimals(2)
        self._dsb_after_split_delay_override.setMinimum(0)
        self._dsb_after_split_delay_override.setMaximum(999)
        self._sb_max_capture_rate.setMinimum(1)
        self._sb_max_capture_rate.setMaximum(999)
        self._sb_max_capture_rate_override.setMinimum(1)
        self._sb_max_capture_rate_override.setMaximum(999)
        self._dsb_after_key_press_delay.setDecimals(2)
        self._dsb_after_key_press_delay.setMinimum(0)
        self._dsb_after_key_press_delay.setMaximum(999)
        self._dsb_after_key_press_delay_override.setDecimals(2)
        self._dsb_after_key_press_delay_override.setMinimum(0)
        self._dsb_after_key_press_delay_override.setMaximum(999)
        self._sb_automatic_threshold_overhead.setMinimum(0)
        self._sb_automatic_threshold_overhead.setMaximum(255)
        self._sb_automatic_threshold_overhead_override.setMinimum(0)
        self._sb_automatic_threshold_overhead_override.setMaximum(255)

        # Add to layout
        button_settings_layout: QFormLayout = QFormLayout()
        button_settings_layout.addRow(self._lbl_split, self._key_picker_split)
        button_settings_layout.addRow(self._lbl_pause, self._key_picker_pause)
        button_settings_layout.addRow(self._lbl_reset, self._key_picker_reset)
        button_settings_layout.addRow(self._lbl_decrement, self._key_picker_decrement)
        button_settings_layout.addRow(self._lbl_increment, self._key_picker_increment)
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
        return button_settings_layout

    def _construct_info_elements(self) -> None:
        self._lbl_info: QLabel = QLabel()
        self._lbl_info.setWordWrap(True)

        self._info_box: QVBoxLayout = QVBoxLayout()
        self._info_box.addWidget(self._lbl_info)

        self._gb_info_highlight: QGroupBox = QGroupBox("Info:")
        self._gb_info_highlight.setLayout(self._info_box)

    def _construct_rect_select_layout(self) -> QVBoxLayout:
        # Initialize
        self._lbl_gray_value: QLabel = QLabel("Avg. Gray Value: -")
        self._gv_preview_image: RectSelectGraphicsView = RectSelectGraphicsView()

        # Setup
        if len(config.get_video_preview_coords()) == 4:
            self._gv_preview_image.set_rect(config.get_video_preview_coords()[0],
                                            config.get_video_preview_coords()[1],
                                            config.get_video_preview_coords()[2],
                                            config.get_video_preview_coords()[3])

        # Add to layout
        rect_select_layout: QVBoxLayout = QVBoxLayout()
        rect_select_layout.addWidget(QLabel("Drag on the preview image to select the region "
                                            "of the screen that should be checked for blackscreens."))
        rect_select_layout.addWidget(self._gv_preview_image)
        rect_select_layout.addWidget(self._lbl_gray_value)
        return rect_select_layout

    ####################
    # Sub-Initializers #
    ####################

    def _init_video_preview_thread(self):
        self._tmr_preview_image: QTimer = QTimer(self)
        self._tmr_preview_image.setInterval(200)
        self._video_preview_thread: QThread = QThread()
        # self._video_preview_worker: SettingsVideoPreviewWorker = SettingsVideoPreviewWorker()
        # self._video_preview_worker.moveToThread(self._video_preview_thread)
        self._tmr_preview_image.moveToThread(self._video_preview_thread)
        # self._tmr_preview_image.timeout.connect(self._video_preview_worker.run)
        # self._video_preview_thread.started.connect(self._tmr_preview_image.start)
        # self._video_preview_worker.gray_value_updated.connect(self._preview_on_gray_value_updated)
        # self._video_preview_worker.image_captured.connect(self._preview_on_image_captured)
        self._video_preview_thread.start()

    def _init_info_timer(self):
        self._tmr_info: QTimer = QTimer(self)
        self._tmr_info.setInterval(200)
        self._tmr_info.timeout.connect(self._on_info_timeout)
        self._tmr_info.start()

    def _load_from_config(self): # TODO: support for overrides
        if config.get_current_splits_profile_path() == "":
            self._btn_change_options_mode.setEnabled(False)
        self._key_picker_split.set_key(config.get_split_key())
        self._key_picker_pause.set_key(config.get_pause_key())
        self._key_picker_reset.set_key(config.get_reset_key())
        self._key_picker_decrement.set_key(config.get_decrement_key())
        self._key_picker_increment.set_key(config.get_increment_key())
        self._sb_blackscreen_threshold.setValue(config.get_blackscreen_threshold())
        self._dsb_after_split_delay.setValue(config.get_after_split_delay())
        self._sb_max_capture_rate.setValue(config.get_max_capture_rate())
        self._dsb_after_key_press_delay.setValue(config.get_after_key_press_delay())
        self._sb_automatic_threshold_overhead.setValue(config.get_automatic_threshold_overhead())

    def _hide_advanced_settings(self):
        self._lbl_max_capture_rate.setVisible(False)
        self._sb_max_capture_rate.setVisible(False)
        self._sb_max_capture_rate_override.setVisible(False)
        self._lbl_after_key_press_delay.setVisible(False)
        self._dsb_after_key_press_delay.setVisible(False)
        self._dsb_after_key_press_delay_override.setVisible(False)
        self._lbl_automatic_threshold_overhead.setVisible(False)
        self._sb_automatic_threshold_overhead.setVisible(False)
        self._sb_automatic_threshold_overhead_override.setVisible(False)

    def _show_advanced_settings(self):
        self._lbl_max_capture_rate.setVisible(True)
        self._sb_max_capture_rate.setVisible(True)
        self._sb_max_capture_rate_override.setVisible(True)
        self._lbl_after_key_press_delay.setVisible(True)
        self._dsb_after_key_press_delay.setVisible(True)
        self._dsb_after_key_press_delay_override.setVisible(True)
        self._lbl_automatic_threshold_overhead.setVisible(True)
        self._sb_automatic_threshold_overhead.setVisible(True)
        self._sb_automatic_threshold_overhead_override.setVisible(True)

    def _disable_override_spin_boxes(self):
        self._sb_blackscreen_threshold_override.setEnabled(False)
        self._dsb_after_split_delay_override.setEnabled(False)
        self._sb_max_capture_rate_override.setEnabled(False)
        self._dsb_after_key_press_delay_override.setEnabled(False)
        self._sb_automatic_threshold_overhead_override.setEnabled(False)

    def _enable_override_spin_boxes(self):
        self._sb_blackscreen_threshold_override.setEnabled(True)
        self._dsb_after_split_delay_override.setEnabled(True)
        self._sb_max_capture_rate_override.setEnabled(True)
        self._dsb_after_key_press_delay_override.setEnabled(True)
        self._sb_automatic_threshold_overhead_override.setEnabled(True)

    #################################
    # Button-/Tooltip functionality #
    #################################

    def _on_info_timeout(self):
        if self._btn_change_options_mode.underMouse():
            if self._global_options_mode_enabled:
                self._lbl_info.setText("Switch to \"per-profile settings override mode\".\n"
                                       "Changes are saved on top of global settings for each splits\n"
                                       "profile individually.")
            else:
                self._lbl_info.setText("Switch to \"global settings mode\".\n"
                                       "Changes are saved to global settings.")
        elif self._btn_restore_defaults.underMouse():
            if self._global_options_mode_enabled:
                self._lbl_info.setText("Restore default settings.\n(NOTE: Key bindings are NOT affected by this.)")
            else:
                self._lbl_info.setText("Clear settings overrides for current profile.\n"
                                       "(NOTE: Key bindings ARE affected by this.)")
        elif self._lbl_split.underMouse() or self._key_picker_split.underMouse():
            self._lbl_info.setText("Key automatically pressed when a blackscreen is detected")
        elif self._lbl_pause.underMouse() or self._key_picker_pause.underMouse():
            self._lbl_info.setText("Key to pause/unpause the blackscreen detection")
        elif self._lbl_reset.underMouse() or self._key_picker_reset.underMouse():
            self._lbl_info.setText("Key to reset the blackscreen counter")
        elif self._lbl_decrement.underMouse() or self._key_picker_decrement.underMouse():
            self._lbl_info.setText("Key to subtract 1 from the blackscreen counter")
        elif self._lbl_increment.underMouse() or self._key_picker_increment.underMouse():
            self._lbl_info.setText("Key to add 1 to the blackscreen counter")
        elif self._btn_automatic_threshold.underMouse():
            self._lbl_info.setText("Enter automatic blackscreen detection mode.")
        elif self._lbl_blackscreen_threshold.underMouse() or self._sb_blackscreen_threshold.underMouse():
            self._lbl_info.setText("Maximum Avg. Gray Value the selected area can have to still be\nconsidered a "
                                   "\"blackscreen\"")
        elif self._lbl_after_split_delay.underMouse() or self._dsb_after_split_delay.underMouse():
            self._lbl_info.setText("Delay after a blackscreen was successfully detected to\nprevent multiple splits "
                                   "per blackscreen")
        elif self._lbl_advanced_settings.underMouse() or self._cb_advanced_settings.underMouse():
            self._lbl_info.setText("The default values for these should work in most cases")
        elif self._lbl_max_capture_rate.underMouse() or self._sb_max_capture_rate.underMouse():
            self._lbl_info.setText(
                "Times/second a capture is taken\n(NOTE: this is a maximum and possibly unreachable)")
        elif self._lbl_after_key_press_delay.underMouse() or self._dsb_after_key_press_delay.underMouse():
            self._lbl_info.setText("Delay after any key press to prevent multiple registrations")
        elif self._lbl_automatic_threshold_overhead.underMouse() or self._sb_automatic_threshold_overhead.underMouse():
            self._lbl_info.setText("Value added to automatically calculated threshold for better tolerance")
        else:
            self._lbl_info.setText("")

        # append instructions for automatic thresholding
        if self._btn_automatic_threshold.isChecked():
            self._lbl_info.setText("Select preview area, wait for a blackscreen to occur, disable automatic\nmode "
                                   "again\n\n" + self._lbl_info.text())

    def _cb_advanced_settings_state_changed(self):
        self._lbl_max_capture_rate.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_max_capture_rate.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_max_capture_rate_override.setVisible(self._cb_advanced_settings.isChecked())
        self._lbl_after_key_press_delay.setVisible(self._cb_advanced_settings.isChecked())
        self._dsb_after_key_press_delay.setVisible(self._cb_advanced_settings.isChecked())
        self._dsb_after_key_press_delay_override.setVisible(self._cb_advanced_settings.isChecked())
        self._lbl_automatic_threshold_overhead.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_automatic_threshold_overhead.setVisible(self._cb_advanced_settings.isChecked())
        self._sb_automatic_threshold_overhead_override.setVisible(self._cb_advanced_settings.isChecked())

    def _btn_box_accepted(self):  # TODO: rework for per-profile-settings
        config.set_split_key(self._key_picker_split.get_global_key())
        config.set_pause_key(self._key_picker_pause.get_global_key())
        config.set_reset_key(self._key_picker_reset.get_global_key())
        config.set_decrement_key(self._key_picker_decrement.get_global_key())
        config.set_increment_key(self._key_picker_increment.get_global_key())
        config.set_blackscreen_threshold(self._sb_blackscreen_threshold.value())
        config.set_after_split_delay(self._dsb_after_split_delay.value())
        # config.set_video_preview_coords(self._gv_preview_image.get_rect())
        config.set_max_capture_rate(self._sb_max_capture_rate.value())
        config.set_after_key_press_delay(self._dsb_after_key_press_delay.value())
        config.set_automatic_threshold_overhead(self._sb_automatic_threshold_overhead.value())
        config.write_config_to_file()
        self.close()

    def _btn_box_rejected(self):
        self.close()

    ###################
    # Event overrides #
    ###################

    def closeEvent(self, event: QCloseEvent) -> None:
        self._tmr_preview_image.stop()
        self._tmr_preview_image.stop()
        self._tmr_info.stop()

        self._video_preview_thread.quit()
        self._video_preview_thread.wait()
        self._video_preview_thread = None
