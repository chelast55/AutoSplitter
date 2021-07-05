from PySide6.QtWidgets import QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QDialog
import os

import Config


class SplitsProfileSelectorDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.resize(700, 400)

        self.layout = QVBoxLayout(self)
        self._tv_directory: QTreeView = QTreeView()
        self.layout.addWidget(self._tv_directory)

        # TODO: Find a more robust way to get the splits_profiles directory
        splits_profiles_dir: str = os.path.join(os.getcwd(), "splits_profiles")

        self._directory_model: QFileSystemModel = QFileSystemModel()
        self._directory_model.setRootPath(splits_profiles_dir)
        self._tv_directory.setModel(self._directory_model)
        self._tv_directory.setRootIndex(self._directory_model.index(splits_profiles_dir))
        self._tv_directory.doubleClicked.connect(self._tv_directory_on_double_click)

        # hide all columns except for "name"
        for i in range(1, self._directory_model.columnCount()):
            self._tv_directory.hideColumn(i)

    def _tv_directory_on_double_click(self):
        selected_index = self._tv_directory.selectedIndexes()[0]
        path = self._directory_model.filePath(selected_index)
        Config.path_to_current_splits_profile = path
        Config.write_config_to_file()
        self.close()
