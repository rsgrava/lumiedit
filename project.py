# This Python file uses the following encoding: utf-8

import os, json

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
        self.save()

    def load(self, dir):
        data = json.loads(open(dir + "/project.json", "r").read())
        self.name = data["name"]
        self.dir = dir
        self.initialized = True

    def save(self):
        data = {}
        data["name"] = self.name
        open(self.dir + "/project.json", "w").write(json.dumps(data))

    def new_tileset(self, type, filename):
        if type == "bg":
            list = self.bg_tilesets
        elif type == "ob":
            list = self.ob_tilesets
        for tileset in list:
            if list[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        name = os.path.splitext(filename)[0].split('/')[-1]
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
