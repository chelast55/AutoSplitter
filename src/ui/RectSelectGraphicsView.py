""" TODO: write something here """

from typing import Optional
from PIL import ImageDraw
from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PySide6.QtCore import QPoint, Signal
from PySide6.QtGui import QMouseEvent, Qt, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


class RectSelectGraphicsView(QGraphicsView):
    """ TODO: write something here """

    rect_set: Signal = Signal()

    def __init__(self):
        super().__init__()

        self._dragging: bool = False
        self._pos1: Optional[QPoint] = None
        self._pos2: Optional[QPoint] = None
        self.img: Optional[Image] = None
        self._internal_img: Optional[Image] = None

    def set_rect(self, left: int, top: int, right: int, bottom: int):
        self._pos1 = QPoint(left, top)
        self._pos2 = QPoint(right, bottom)
        self._draw_overlay()

    def get_rect(self) -> tuple[int, int, int, int]:
        return (min(self._pos1.x(), self._pos2.x()),
                min(self._pos1.y(), self._pos2.y()),
                max(self._pos1.x(), self._pos2.x()),
                max(self._pos1.y(), self._pos2.y()))

    def has_area(self) -> bool:
        """
        :return: True, if the stored rectangle has an area > 0
        """
        if self._pos1 is None or self._pos2 is None:
            return False

        rect: tuple[int, int, int, int] = self.get_rect()
        return rect[2] - rect[1] >= 1 and rect[3] - rect[1] >= 1

    def set_image(self, img: Image):
        self.img = img
        self._draw_overlay()

    def _draw_overlay(self):
        if self.img is None:
            self.setScene(QGraphicsScene())
            return

        scene: QGraphicsScene = QGraphicsScene()
        internal_img: Image = self.img.copy()

        if self._pos1 is not None and self._pos2 is not None:
            overlay: ImageDraw = ImageDraw.Draw(internal_img, "RGBA")
            overlay.rectangle(
                (
                    (self.get_rect()[0], self.get_rect()[1]),
                    (self.get_rect()[2], self.get_rect()[3])
                ),
                None,
                "#FF0000FF",
                width=5
            )

        pixmap: QPixmap = QPixmap.fromImage(ImageQt(internal_img))
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.setScene(scene)
        self.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() != Qt.LeftButton:
            return

        self._dragging = True
        self._pos1 = self.mapToScene(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() != Qt.LeftButton:
            return

        self._dragging = False
        self.rect_set.emit()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self._dragging:
            return

        self._pos2 = self.mapToScene(event.pos())
        self._draw_overlay()
