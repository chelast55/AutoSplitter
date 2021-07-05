from PySide6.QtCore import QPointF, Signal, QObject
from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QGraphicsView


class QRectSelectGraphicsView(QGraphicsView):

    rect_set = Signal()

    def __init__(self):
        super().__init__()

        self.pos1: QPointF = None
        self.pos2: QPointF = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return

        self.pos1 = self.mapToScene(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return

        self.pos2 = self.mapToScene(event.pos())
        self.rect_set.emit()

