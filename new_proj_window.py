# This Python file uses the following encoding: utf-8

import os

from PySide6.QtWidgets import QDialog, QFileDialog
from ui_new_proj_window import Ui_NewProjWindow

class NewProjWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NewProjWindow()
        self.ui.setupUi(self)
        self.ui.dir_btn.clicked.connect(self.choose_dir)
        self.ui.dir_edit.setText(os.path.expanduser("~/Documents/lumiedit/projects/Project"))

    def get_text(self):
        ok = super().exec()
        if not ok == QDialog.Accepted:
            return False, "", ""
        name = self.ui.name_edit.text()
        dir = self.ui.dir_edit.text()
        if not name or not dir:
            raise Exception("Please input a name and directory!")
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not len(os.listdir(dir)) == 0:
            raise Exception("Directory is not empty!")
        return True, name, dir

    def choose_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Choose Directory", os.path.expanduser("~/Documents/lumiedit/projects/Project"), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir:
            self.ui.dir_edit.setText(dir)
