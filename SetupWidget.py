from typing import List

from PIL import ImageGrab
from PIL.Image import Image
from PIL import ImageDraw
from PIL.ImageQt import ImageQt
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QCloseEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QDialogButtonBox, QSpinBox, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem, QLabel

import Config
import ImageAnalyzer
from KeyPickerWidget import KeyPickerWidget
from QRectSelectGraphicsView import QRectSelectGraphicsView
import StringHelper


class SetupWidget(QWidget):

    def __init__(self):
        super(SetupWidget, self).__init__()

        self.setWindowTitle("Settings")
        self.resize(1400, 600)

        self._tmr_preview_image: QTimer = QTimer(self)
        self._tmr_preview_image.timeout.connect(self._tmr_preview_image_on_timeout)
        self._tmr_preview_image.start(200)

        self._gv_preview_image: QRectSelectGraphicsView = QRectSelectGraphicsView()
        self._btn_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self._key_picker_split: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_pause: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_reset: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_decrement: KeyPickerWidget = KeyPickerWidget()
        self._key_picker_increment: KeyPickerWidget = KeyPickerWidget()
        self._sb_blackscreen_threshold: QSpinBox = QSpinBox()
        self._sb_blackscreen_threshold.setMinimum(0)
        self._sb_blackscreen_threshold.setMaximum(255)
        self._sb_after_split_delay: QSpinBox = QSpinBox()
        self._sb_after_split_delay.setMinimum(0)
        self._sb_after_split_delay.setMaximum(999)

        self._key_picker_split.set_key(Config.split_key)
        self._key_picker_pause.set_key(Config.pause_key)
        self._key_picker_reset.set_key(Config.reset_key)
        self._key_picker_decrement.set_key(Config.decrement_key)
        self._key_picker_increment.set_key(Config.increment_key)
        self._sb_blackscreen_threshold.setValue(Config.blackscreen_threshold)
        self._sb_after_split_delay.setValue(Config.after_split_delay)
        self._gv_preview_image.set_rect(Config.video_preview_coords[0],
                                        Config.video_preview_coords[1],
                                        Config.video_preview_coords[2],
                                        Config.video_preview_coords[3])

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
        button_settings_layout.addRow("After Split Delay (s):", self._sb_after_split_delay)
        settings_layout.addLayout(button_settings_layout)

        rect_select_layout: QVBoxLayout = QVBoxLayout()
        rect_select_layout.addWidget(QLabel("Drag on the preview image to select the region "
                                            "of the screen that should be checked for blackscreens."))
        rect_select_layout.addWidget(self._gv_preview_image)
        self._lbl_gray_value: QLabel = QLabel("Avg. Gray Value: -")
        rect_select_layout.addWidget(self._lbl_gray_value)
        settings_layout.addLayout(rect_select_layout)

        self.layout.addLayout(settings_layout)

        self._btn_box.accepted.connect(self._btn_box_accepted)
        self._btn_box.rejected.connect(self._btn_box_rejected)
        self.layout.addWidget(self._btn_box)

    def _tmr_preview_image_on_timeout(self):
        img: Image = ImageGrab.grab(all_screens=True)
        self._gv_preview_image.set_image(img)
        cropped_img = img.crop(Config.video_preview_coords)
        gray_value = ImageAnalyzer.average_black_value(cropped_img)  # TODO: add some kind of tolerance variable
        self._lbl_gray_value.setText("Avg. Gray Value: " + str(gray_value))

    def _btn_box_accepted(self):
        Config.split_key = self._key_picker_split.key
        Config.pause_key = self._key_picker_pause.key
        Config.reset_key = self._key_picker_reset.key
        Config.decrement_key = self._key_picker_decrement.key
        Config.increment_key = self._key_picker_increment.key
        Config.blackscreen_threshold = self._sb_blackscreen_threshold.value()
        Config.after_split_delay = self._sb_after_split_delay.value()
        Config.video_preview_coords = self._gv_preview_image.get_rect()
        Config.write_config_to_file()
        self.close()

    def _btn_box_rejected(self):
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._tmr_preview_image.stop()
