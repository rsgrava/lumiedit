# This Python file uses the following encoding: utf-8
import sys, os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFileDialog, QGraphicsScene, QListWidgetItem
from PySide6.QtGui import QBrush

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

        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)

        self.ui.bg_tileset_list.currentRowChanged.connect(self.select_bg_tileset)
        self.ui.ob_tileset_list.currentRowChanged.connect(self.select_ob_tileset)
        self.ui.bg_tileset_list.itemChanged.connect(self.rename_bg_tileset)
        self.ui.ob_tileset_list.itemChanged.connect(self.rename_ob_tileset)

        self.ui.subtile_view.setScene(QGraphicsScene(0, 0, 64, 64))
        self.ui.palette_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette0_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette1_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette2_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette3_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette4_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette5_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette6_view.setScene(QGraphicsScene(0, 0, 128, 32))
        self.ui.palette7_view.setScene(QGraphicsScene(0, 0, 128, 32))

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
        self.tileset_scene.set_rect()

        self.ui.subtile_view.scene().clear()
        self.ui.palette_view.scene().clear()
        self.ui.palette0_view.scene().clear()
        self.ui.palette1_view.scene().clear()
        self.ui.palette2_view.scene().clear()
        self.ui.palette3_view.scene().clear()
        self.ui.palette4_view.scene().clear()
        self.ui.palette5_view.scene().clear()
        self.ui.palette6_view.scene().clear()
        self.ui.palette7_view.scene().clear()

        self.ui.tile_label.setText("Tile: -")
        self.ui.subtile_label.setText("Subtile: -")
        self.ui.palette_label.setText("Palette: -")

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
            self.tileset_scene.tileset = tileset
            self.tileset_scene.setSceneRect(0, 0, tileset.width * 4, tileset.height * 4)
            for tile in tileset.tiles:
                item = self.tileset_scene.addPixmap(tile.image)
                item.setScale(4 * item.scale())
                item.setPos(tile.x * 4, tile.y * 4)
                self.tileset_scene.addRect(tile.x * 4, tile.y * 4, 16 * 4, 16 * 4)

            brush = QBrush(tileset.palettes[0][0])
            self.ui.palette0_view.scene().addRect(0, 0, 32, 32, brush=brush)
            brush.setColor(tileset.palettes[0][1])
            self.ui.palette0_view.scene().addRect(32, 0, 32, 32, brush=brush)
            brush.setColor(tileset.palettes[0][2])
            self.ui.palette0_view.scene().addRect(64, 0, 32, 32, brush=brush)
            brush.setColor(tileset.palettes[0][3])
            self.ui.palette0_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 1:
                brush.setColor(tileset.palettes[1][0])
                self.ui.palette1_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[1][1])
                self.ui.palette1_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[1][2])
                self.ui.palette1_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[1][3])
                self.ui.palette1_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 2:
                brush.setColor(tileset.palettes[2][0])
                self.ui.palette2_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[2][1])
                self.ui.palette2_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[2][2])
                self.ui.palette2_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[2][3])
                self.ui.palette2_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 3:
                brush.setColor(tileset.palettes[3][0])
                self.ui.palette3_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[3][1])
                self.ui.palette3_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[3][2])
                self.ui.palette3_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[3][3])
                self.ui.palette3_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 4:
                brush.setColor(tileset.palettes[4][0])
                self.ui.palette4_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[4][1])
                self.ui.palette4_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[4][2])
                self.ui.palette4_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[4][3])
                self.ui.palette4_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 5:
                brush.setColor(tileset.palettes[5][0])
                self.ui.palette5_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[5][1])
                self.ui.palette5_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[5][2])
                self.ui.palette5_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[5][3])
                self.ui.palette5_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 6:
                brush.setColor(tileset.palettes[6][0])
                self.ui.palette6_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[6][1])
                self.ui.palette6_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[6][2])
                self.ui.palette6_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[6][3])
                self.ui.palette6_view.scene().addRect(96, 0, 32, 32, brush=brush)

            if len(tileset.palettes) > 7:
                brush.setColor(tileset.palettes[7][0])
                self.ui.palette7_view.scene().addRect(0, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[7][1])
                self.ui.palette7_view.scene().addRect(32, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[7][2])
                self.ui.palette7_view.scene().addRect(64, 0, 32, 32, brush=brush)
                brush.setColor(tileset.palettes[7][3])
                self.ui.palette7_view.scene().addRect(96, 0, 32, 32, brush=brush)

    def enable_all_tabs(self):
        for i in range(1, self.ui.tabs.count() + 1):
            self.ui.tabs.setTabEnabled(i, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
