from PySide6 import QtWidgets

# qt app needs to be constructed before we can do anything else with qt
app = QtWidgets.QApplication([])

from src.MainWidget import MainWidget


if __name__ == '__main__':
    widget = MainWidget()
    widget.resize(400, 150)
    widget.show()

    # exit when main window is closed
    exit(app.exec())
