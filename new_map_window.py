# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QIntValidator

from ui_new_map_window import Ui_NewMapWindow

class NewMapWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NewMapWindow()
        self.ui.setupUi(self)
        self.ui.width_edit.setValidator(QIntValidator(10, 256))
        self.ui.height_edit.setValidator(QIntValidator(8, 256))

    def getInput(self):
        ok = super().exec()
        if not ok == QDialog.Accepted:
            return False, None, None, 0, 0
        name = self.ui.name_edit.text()
        tileset = self.ui.tilesets_combo.currentText()
        width = self.ui.width_edit.text()
        height = self.ui.width_edit.text()
        if not name:
            raise Exception("Please input a name!")
        if not tileset:
            raise Exception("Please pick a tileset!")
        if not width:
            raise Exception("Please input width!")
        if not height:
            raise Exception("Please input height!")
        if int(width) * int(height) > 1024:
            raise Exception("Max area exceeded! (max 1024 tiles)")
        return True, name, self.tilesets[tileset], int(width), int(height)

    def setTilesets(self, tilesets):
        self.tilesets = tilesets
        self.ui.tilesets_combo.addItems(list(tilesets.keys()))
