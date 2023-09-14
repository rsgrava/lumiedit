# This Python file uses the following encoding: utf-8

import os, json

from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

from map import Map
from tileset import Tileset

class Project:
    def __init__(self):
        self.name = None
        self.dir = None
        self.initialized = False
        self.unsaved_changes = False
        self.data = {}
        self.bg_tilesets = {}
        self.ob_tilesets = {}
        self.maps = {}

    def new(self, name, dir):
        self.name = name
        self.dir = dir
        self.initialized = True
        self.unsaved_changes = False
        os.makedirs(self.dir + "/tilesets/bg")
        os.makedirs(self.dir + "/tilesets/ob")
        os.makedirs(self.dir + "/maps")
        self.save()

    def load(self, ui, dir):
        data = json.loads(open(dir + "/project.json", "r").read())

        self.name = data["name"]
        self.dir = dir

        for name, filename in zip(data["bg_tilesets"]["names"], data["bg_tilesets"]["filenames"]):
            self.new_tileset("bg", name, filename)
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            ui.bg_tileset_list.addItem(item)

        for name, filename in zip(data["ob_tilesets"]["names"], data["ob_tilesets"]["filenames"]):
            self.new_tileset("ob", name, filename)
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            ui.ob_tileset_list.addItem(item)

        self.initialized = True
        self.unsaved_changes = False

    def save(self):
        data = {}

        data["name"] = self.name

        filenames = []
        for bg in self.bg_tilesets:
            filenames.append(self.bg_tilesets[bg].filename)
        data["bg_tilesets"] = {}
        data["bg_tilesets"]["names"] = list(self.bg_tilesets.keys())
        data["bg_tilesets"]["filenames"] = filenames

        filenames = []
        for ob in self.ob_tilesets:
            filenames.append(self.ob_tilesets[ob].filename)
        data["ob_tilesets"] = {}
        data["ob_tilesets"]["names"] = list(self.ob_tilesets.keys())
        data["ob_tilesets"]["filenames"] = filenames

        open(self.dir + "/project.json", "w").write(json.dumps(data))
        self.unsaved_changes = False

    def new_tileset(self, type, name, filename):
        if type == "bg":
            list = self.bg_tilesets
        elif type == "ob":
            list = self.ob_tilesets
        for tileset in list:
            if list[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        if name in list:
            raise Exception("Tileset with this name already loaded!")
        list[name] = Tileset(filename)
        self.unsaved_changes = True

    def rename_tileset(self, type, item):
        if type == "bg":
            lst = self.bg_tilesets
        elif type == "ob":
            lst = self.ob_tilesets
        new_name = item.text()
        old_items = lst.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        if new_name in old_items:
            item.setText(old_name)
            return
        lst[new_name] = lst[old_name]
        del lst[old_name]
        self.unsaved_changes = True

    def delete_tileset(self, type, ui):
        if type == "bg":
            del self.bg_tilesets[ui.bg_tileset_list.currentItem().text()]
        elif type == "ob":
            del self.ob_tilesets[ui.ob_tileset_list.currentItem().text()]
        self.unsaved_changes = True

    def new_map(self, name, tileset):
        if name in self.maps:
            raise Exception("Map with this name already exists!")
        self.maps[name] = Map(tileset)
        self.unsaved_changes = True

    def delete_map(self, name):
        del self.maps[name]
        self.unsaved_changes = True
