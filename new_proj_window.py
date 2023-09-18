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
        self.ui.output_dir_btn.clicked.connect(self.choose_output_dir)
        self.ui.name_edit.setText("Project")
        self.ui.dir_edit.setText(os.path.expanduser("~/Documents/lumiedit/projects/Project"))
        self.ui.output_dir_edit.setText(os.path.expanduser("~/Documents/lumiedit/projects/Project/out"))

    def get_text(self):
        ok = super().exec()
        if not ok == QDialog.Accepted:
            return False, "", "", ""
        name = self.ui.name_edit.text()
        dir = self.ui.dir_edit.text()
        output_dir = self.ui.output_dir_edit.text()
        if not name or not dir or not output_dir:
            raise Exception("Please input a name and directories!")
        os.makedirs(dir, exist_ok=True)
        if not len(os.listdir(dir)) == 0:
            raise Exception("Project directory is not empty!")
        return True, name, dir, output_dir

    def choose_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Choose Directory", os.path.expanduser("~/Documents/lumiedit/projects"), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir:
            self.ui.dir_edit.setText(dir)

    def choose_output_dir(self):
        dir = QFileDialog.getExistingDirectory(self, "Choose Directory", os.path.expanduser("~/Documents/lumiedit/projects"), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir:
            self.ui.output_dir.setText(dir)
