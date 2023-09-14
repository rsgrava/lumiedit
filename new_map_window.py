# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QDialog

from ui_new_map_window import Ui_NewMapWindow

class NewMapWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_NewMapWindow()
        self.ui.setupUi(self)

    def getInput(self):
        ok = super().exec()
        if not ok == QDialog.Accepted:
            return False, None, None
        name = self.ui.name_edit.text()
        tileset = self.ui.tilesets_combo.currentText()
        if not name:
            raise Exception("Please input a name!")
        if not tileset:
            raise Exception("Please pick a tileset!")
        return True, name, self.tilesets[tileset]

    def setTilesets(self, tilesets):
        self.tilesets = tilesets
        self.ui.tilesets_combo.addItems(list(tilesets.keys()))
