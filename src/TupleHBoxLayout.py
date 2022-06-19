from PySide6.QtWidgets import QHBoxLayout, QWidget


class TupleHBoxLayout(QHBoxLayout):
    """
    Child of QHBoxLayout containing exactly 2 QWidgets
    """

    def __init__(self, w1: QWidget, w2: QWidget):
        super().__init__()

        self.addWidget(w1)
        self.addWidget(w2)
