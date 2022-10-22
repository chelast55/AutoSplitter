from PySide6.QtWidgets import QApplication, QWidget

# qt app needs to be constructed before we can do anything else with qt
app: QApplication = QApplication([])

from ui.MainWidget import MainWidget


if __name__ == '__main__':
    widget: QWidget = MainWidget()
    widget.resize(400, 150)
    widget.show()

    # exit when main window is closed
    exit(app.exec())
