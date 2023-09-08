# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox

from ui_main import Ui_MainWindow
from project import Project

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("lumiedit")
        self.project = None

        self.ui.new_project_btn.clicked.connect(self.new_project)
        self.ui.load_project_btn.clicked.connect(self.load_project)
        self.ui.new_tileset_btn.clicked.connect(self.new_tileset)

    def new_project(self):
        name, ok = QInputDialog().getText(self, "Insert Project Name", "Project name:")
        if ok and name:
            self.project = Project(name)
            self.setWindowTitle("lumiedit - " + name)
            self.ui.project_label.setText("Current project: " + name)
            self.enable_all_tabs()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid project name!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def load_project(self):
        ...

    def new_tileset(self):
        ...

    def enable_all_tabs(self):
        for i in range(1, self.ui.tabs.count() + 1):
            self.ui.tabs.setTabEnabled(i, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
