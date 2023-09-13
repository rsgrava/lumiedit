# This Python file uses the following encoding: utf-8
import sys, os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFileDialog, QGraphicsScene, QListWidgetItem

from ui_main import Ui_MainWindow
from project import Project
from tileset_scene import TilesetScene

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("lumiedit")
        self.project = Project()

        self.ui.new_project_btn.clicked.connect(self.new_project)
        self.ui.new_bg_tileset_btn.clicked.connect(self.new_bg_tileset)
        self.ui.new_ob_tileset_btn.clicked.connect(self.new_ob_tileset)
        self.ui.delete_bg_tileset_btn.clicked.connect(self.delete_bg_tileset)
        self.ui.delete_ob_tileset_btn.clicked.connect(self.delete_ob_tileset)

        self.ui.bg_tileset_list.currentRowChanged.connect(self.select_bg_tileset)
        self.ui.ob_tileset_list.currentRowChanged.connect(self.select_ob_tileset)
        self.ui.bg_tileset_list.itemChanged.connect(self.rename_bg_tileset)
        self.ui.ob_tileset_list.itemChanged.connect(self.rename_ob_tileset)

        self.ui.tile_view.setScene(QGraphicsScene(0, 0, 64, 64))
        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)

    def new_project(self):
        name, ok = QInputDialog().getText(self, "Insert Project Name", "Project name:")
        if ok and name:
            self.project = Project()
            self.project.new(name)
            self.ui.bg_tileset_list.clear()
            self.ui.ob_tileset_list.clear()
            self.setWindowTitle("lumiedit - " + name)
            self.ui.project_label.setText("Current project: " + name)
            self.enable_all_tabs()

    def new_bg_tileset(self):
        filename = QFileDialog.getOpenFileName(caption="Open Tileset")[0]
        if filename:
            try:
                self.project.new_bg_tileset(filename)
                item = QListWidgetItem(os.path.splitext(filename)[0].split('/')[-1])
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.ui.bg_tileset_list.addItem(item)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(str(e))
                msg.setWindowTitle("Error")
                msg.exec()

    def new_ob_tileset(self):
        filename = QFileDialog.getOpenFileName(caption="Open Tileset")[0]
        if filename:
            try:
                self.project.new_ob_tileset(filename)
                item = QListWidgetItem(os.path.splitext(filename)[0].split('/')[-1])
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.ui.ob_tileset_list.addItem(item)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(str(e))
                msg.setWindowTitle("Error")
                msg.exec()

    def rename_bg_tileset(self, item):
        self.ui.bg_tileset_list.blockSignals(True)
        self.project.rename_bg_tileset(item)
        self.ui.bg_tileset_list.blockSignals(False)

    def rename_ob_tileset(self, item):
        self.ui.ob_tileset_list.blockSignals(True)
        self.project.rename_ob_tileset(item)
        self.ui.ob_tileset_list.blockSignals(False)

    def delete_bg_tileset(self):
        if self.ui.bg_tileset_list.currentItem() == None:
            return
        self.project.delete_bg_tileset(self.ui)
        self.ui.bg_tileset_list.takeItem(self.ui.bg_tileset_list.currentRow())
        self.ui.bg_tileset_list.clearSelection()
        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)

    def delete_ob_tileset(self):
        if self.ui.ob_tileset_list.currentItem() == None:
            return
        self.project.delete_ob_tileset(self.ui)
        self.ui.ob_tileset_list.takeItem(self.ui.ob_tileset_list.currentRow())
        self.ui.ob_tileset_list.clearSelection()
        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)

    def select_bg_tileset(self):
        self.refresh_tileview("bg")
        self.ui.ob_tileset_list.clearSelection()

    def select_ob_tileset(self):
        self.refresh_tileview("ob")
        self.ui.bg_tileset_list.clearSelection()

    def refresh_tileview(self, type):
        self.tileset_scene.clear()
        match type:
            case "bg":
                current_item = self.ui.bg_tileset_list.currentItem()
            case "ob":
                current_item = self.ui.ob_tileset_list.currentItem()
        if current_item:
            match type:
                case "bg":
                    tileset = self.project.bg_tilesets[current_item.text()]
                case "ob":
                    tileset = self.project.ob_tilesets[current_item.text()]
            self.tileset_scene.setTileset(tileset)

    def enable_all_tabs(self):
        for i in range(1, self.ui.tabs.count() + 1):
            self.ui.tabs.setTabEnabled(i, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
