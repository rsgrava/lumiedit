# This Python file uses the following encoding: utf-8
import sys, os, json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QGraphicsScene, QListWidgetItem

from ui_main import Ui_MainWindow
from map_editor import MapEditor
from new_map_window import NewMapWindow
from new_proj_window import NewProjWindow
from project import Project
from tile_select_scene import TileSelectScene
from tileset_scene import TilesetScene

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("lumiedit")

        os.makedirs(os.path.expanduser("~/Documents/lumiedit"), exist_ok=True)
        os.makedirs(os.path.expanduser("~/Documents/lumiedit/projects"), exist_ok=True)
        try:
            self.cfg = json.loads(open(os.path.expanduser("~/Documents/lumiedit/cfg.json"), "r").read())
        except:
            self.cfg = {
                "last_project": None
            }
            self.write_cfg()

        self.project = Project()
        if self.cfg["last_project"]:
            try:
                self.project.load(self.ui, self.cfg["last_project"])
                self.set_proj_labels()
                self.enable_all_tabs()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "Failed to read last project: " + self.cfg["last_project"] + "\n\n" +
                    str(e)
                )
                msg.setWindowTitle("Error")
                msg.exec()

        self.ui.new_project_btn.clicked.connect(self.new_project)
        self.ui.load_project_btn.clicked.connect(self.load_project)
        self.ui.save_project_btn.clicked.connect(self.save_project)
        self.ui.compile_project_btn.clicked.connect(self.compile_project)
        self.ui.set_output_dir_btn.clicked.connect(self.set_output_dir)

        self.ui.new_bg_tileset_btn.clicked.connect(self.new_bg_tileset)
        self.ui.new_ob_tileset_btn.clicked.connect(self.new_ob_tileset)
        self.ui.delete_bg_tileset_btn.clicked.connect(self.delete_bg_tileset)
        self.ui.delete_ob_tileset_btn.clicked.connect(self.delete_ob_tileset)

        self.ui.new_map_btn.clicked.connect(self.new_map)
        self.ui.delete_map_btn.clicked.connect(self.delete_map)
        self.ui.hflip_box.toggled.connect(self.hflip_toggled)
        self.ui.vflip_box.toggled.connect(self.vflip_toggled)

        self.ui.bg_tileset_list.currentRowChanged.connect(self.select_bg_tileset)
        self.ui.ob_tileset_list.currentRowChanged.connect(self.select_ob_tileset)
        self.ui.map_list.currentRowChanged.connect(self.select_map)

        self.ui.bg_tileset_list.itemChanged.connect(self.rename_bg_tileset)
        self.ui.ob_tileset_list.itemChanged.connect(self.rename_ob_tileset)
        self.ui.map_list.itemChanged.connect(self.rename_map)

        self.ui.tile_view.setScene(QGraphicsScene(0, 0, 64, 64))
        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)
        self.tile_select_scene = TileSelectScene(self.ui.hflip_box, self.ui.vflip_box)
        self.ui.tile_select_view.setScene(self.tile_select_scene)
        self.map_editor = MapEditor(self.tile_select_scene, self.ui.hflip_box, self.ui.vflip_box)
        self.ui.map_editor.setScene(self.map_editor)

    def write_cfg(self):
        open(os.path.expanduser("~/Documents/lumiedit/cfg.json"), "w").write(json.dumps(self.cfg))

    def set_proj_labels(self):
        self.setWindowTitle("lumiedit - " + self.project.name)
        self.ui.proj_name_label.setText("Current project: " + self.project.name)
        self.ui.proj_dir_label.setText("Project directory: " + self.project.dir)
        self.ui.output_dir_label.setText("Output directory: " + self.project.output_dir)

    def clear_project(self):
        self.ui.bg_tileset_list.clear()
        self.ui.ob_tileset_list.clear()
        self.ui.map_list.clear()

    def new_project(self):
        try:
            ok, name, dir, output_dir = NewProjWindow().get_text()
            if not ok:
                return
            self.project = Project()
            self.project.new(name, dir, output_dir)
            self.cfg["last_project"] = dir
            self.clear_project()
            self.set_proj_labels()
            self.enable_all_tabs()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setWindowTitle("Error")
            msg.exec()

    def load_project(self):
        dir = QFileDialog().getExistingDirectory(self, "Choose Directory", os.path.expanduser("~/Documents/lumiedit/projects/"), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir:
            try:
                self.clear_project()
                self.project.load(self.ui, dir)
                self.cfg["last_project"] = dir
                self.set_proj_labels()
                self.enable_all_tabs()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Failed to load project!\n\n" + str(e))
                msg.setWindowTitle("Error")
                msg.exec()

    def save_project(self):
        if self.project.initialized:
            try:
                self.project.save()
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Failed to save project!\n\n" + str(e))
                msg.setWindowTitle("Error")
                msg.exec()

    def compile_project(self):
        try:
            self.project.compile()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Project compiled successfully.")
            msg.setWindowTitle("Success")
            msg.exec()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Failed to save project!\n\n" + str(e))
            msg.setWindowTitle("Error")
            msg.exec()

    def set_output_dir(self):
        dir = QFileDialog().getExistingDirectory(self, "Choose Directory", self.project.output_dir, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.project.set_output_dir(dir)
        self.set_proj_labels()

    def new_tileset(self, type):
        if type == "bg":
            filename = QFileDialog.getOpenFileName(caption="Open Tileset", dir=self.project.dir + "/tilesets/bg")[0]
        elif type == "ob":
            filename = QFileDialog.getOpenFileName(caption="Open Tileset", dir=self.project.dir + "/tilesets/ob")[0]
        if filename:
            try:
                name = os.path.splitext(filename)[0].split('/')[-1]
                self.project.new_tileset(type, name, filename)
                item = QListWidgetItem(name)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                if type == "bg":
                    self.ui.bg_tileset_list.addItem(item)
                elif type == "ob":
                    self.ui.ob_tileset_list.addItem(item)
            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(str(e))
                msg.setWindowTitle("Error")
                msg.exec()

    def new_bg_tileset(self):
        self.new_tileset("bg")

    def new_ob_tileset(self):
        self.new_tileset("ob")

    def rename_bg_tileset(self, item):
        self.ui.bg_tileset_list.blockSignals(True)
        self.project.rename_tileset("bg", item)
        self.ui.bg_tileset_list.blockSignals(False)

    def rename_ob_tileset(self, item):
        self.ui.ob_tileset_list.blockSignals(True)
        self.project.rename_tileset("ob", item)
        self.ui.ob_tileset_list.blockSignals(False)

    def delete_tileset(self, type):
        try:
            if type == "bg":
                list = self.ui.bg_tileset_list
                self.project.delete_tileset("bg", list.currentItem().text())
            elif type == "ob":
                list = self.ui.ob_tileset_list
                self.project.delete_tileset("ob", list.currentItem().text())
            list.takeItem(list.currentRow())
            list.clearSelection()
            self.tileset_scene = TilesetScene(self.ui)
            self.ui.tileset_view.setScene(self.tileset_scene)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setWindowTitle("Error")
            msg.exec()

    def delete_bg_tileset(self):
        if self.ui.bg_tileset_list.currentItem() == None:
            return
        self.delete_tileset("bg")

    def delete_ob_tileset(self):
        if self.ui.ob_tileset_list.currentItem() == None:
            return
        self.delete_tileset("ob")

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

    def new_map(self):
        window = NewMapWindow()
        window.setTilesets(self.project.bg_tilesets)
        try:
            ok, name, tileset, width, height = window.getInput()
            if ok:
                self.project.new_map(name, tileset, width, height)
                item = QListWidgetItem(name)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.ui.map_list.addItem(item)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setWindowTitle("Error")
            msg.exec()

    def rename_map(self, item):
        self.ui.map_list.blockSignals(True)
        self.project.rename_map(item)
        self.ui.map_list.blockSignals(False)

    def delete_map(self):
        if self.ui.map_list.currentItem() == None:
            return
        result = QMessageBox.question(
            None,
            "Confirmation",
            "Are you sure you want to delete this map?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if result == QMessageBox.Yes:
            self.project.delete_map(self.ui.map_list.currentItem().text())
            self.ui.map_list.takeItem(self.ui.map_list.currentRow())
            self.ui.map_list.clearSelection()
            self.tile_select_scene.clear()
            self.map_editor.clear()

    def select_map(self):
        self.tile_select_scene.clear()
        current_item = self.ui.map_list.currentItem()
        if current_item:
            map = self.project.maps[current_item.text()]
            self.tile_select_scene.set_tileset(map.tileset)
            self.map_editor.set_map(map)

    def hflip_toggled(self, checked):
        self.tile_select_scene.refresh()

    def vflip_toggled(self, checked):
        self.tile_select_scene.refresh()

    def resizeEvent(self, event):
        self.tile_select_scene.refresh()
        self.map_editor.refresh()

    def closeEvent(self, event):
        self.write_cfg()
        if self.project.unsaved_changes:
            msg = QMessageBox()
            msg.setText("Do you want to save the project?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            match msg.exec():
                case QMessageBox.Save:
                    self.save_project()
                case QMessageBox.Cancel:
                    event.ignore()
                    return
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
