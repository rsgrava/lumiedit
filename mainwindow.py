# This Python file uses the following encoding: utf-8
import sys, os, json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QFileDialog, QGraphicsScene, QListWidgetItem

from ui_main import Ui_MainWindow
from new_map_window import NewMapWindow
from new_proj_window import NewProjWindow
from project import Project
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
        self.ui.new_bg_tileset_btn.clicked.connect(self.new_bg_tileset)
        self.ui.new_ob_tileset_btn.clicked.connect(self.new_ob_tileset)
        self.ui.delete_bg_tileset_btn.clicked.connect(self.delete_bg_tileset)
        self.ui.delete_ob_tileset_btn.clicked.connect(self.delete_ob_tileset)
        self.ui.new_map_btn.clicked.connect(self.new_map)
        self.ui.delete_map_btn.clicked.connect(self.delete_map)

        self.ui.bg_tileset_list.currentRowChanged.connect(self.select_bg_tileset)
        self.ui.ob_tileset_list.currentRowChanged.connect(self.select_ob_tileset)
        self.ui.map_list.currentRowChanged.connect(self.select_map)

        self.ui.bg_tileset_list.itemChanged.connect(self.rename_bg_tileset)
        self.ui.ob_tileset_list.itemChanged.connect(self.rename_ob_tileset)
        self.ui.map_list.itemChanged.connect(self.rename_map)

        self.ui.tile_view.setScene(QGraphicsScene(0, 0, 64, 64))
        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)

    def write_cfg(self):
        open(os.path.expanduser("~/Documents/lumiedit/cfg.json"), "w").write(json.dumps(self.cfg))

    def set_proj_labels(self):
        self.setWindowTitle("lumiedit - " + self.project.name)
        self.ui.proj_name_label.setText("Current project: " + self.project.name)
        self.ui.proj_dir_label.setText("Project directory: " + self.project.dir)

    def clear_project(self):
        self.ui.bg_tileset_list.clear()
        self.ui.ob_tileset_list.clear()
        self.ui.map_list.clear()

    def new_project(self):
        try:
            ok, name, dir = NewProjWindow().get_text()
            if not ok:
                return
            self.project = Project()
            self.project.new(name, dir)
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
        if type == "bg":
            self.project.delete_tileset("bg", self.ui)
            list = self.ui.bg_tileset_list
        elif type == "ob":
            self.project.delete_tileset("ob", self.ui)
            list = self.ui.ob_tileset_list
        list.takeItem(list.currentRow())
        list.clearSelection()
        self.tileset_scene = TilesetScene(self.ui)
        self.ui.tileset_view.setScene(self.tileset_scene)

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
            ok, name, tileset = window.getInput()
            if ok and name and tileset:
                self.project.new_map(name, tileset)
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
        ...

    def delete_map(self):
        ...

    def select_map(self):
        ...

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
