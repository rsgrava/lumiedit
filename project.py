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

    def new_bg_tileset(self, filename):
        for tileset in self.bg_tilesets:
            if self.bg_tilesets[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        name = os.path.splitext(filename)[0].split('/')[-1]
        if name in self.bg_tilesets:
            raise Exception("Tileset with this name already loaded!")
        self.bg_tilesets[name] = Tileset(filename)
        self.unsaved_changes = True

    def new_ob_tileset(self, filename):
        for tileset in self.ob_tilesets:
            if self.ob_tilesets[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        name = os.path.splitext(filename)[0].split('/')[-1]
        if name in self.ob_tilesets:
            raise Exception("Tileset with this name already loaded!")
        self.ob_tilesets[name] = Tileset(filename)
        self.unsaved_changes = True

    def rename_bg_tileset(self, item):
        new_name = item.text()
        old_items = self.bg_tilesets.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        if new_name in old_items:
            item.setText(old_name)
            return
        self.bg_tilesets[new_name] = self.bg_tilesets[old_name]
        del self.bg_tilesets[old_name]
        self.unsaved_changes = True

    def rename_ob_tileset(self, item):
        new_name = item.text()
        old_items = self.ob_tilesets.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        if new_name in old_items:
            item.setText(old_name)
            return
        self.ob_tilesets[new_name] = self.ob_tilesets[old_name]
        del self.ob_tilesets[old_name]
        self.unsaved_changes = True

    def delete_bg_tileset(self, ui):
        del self.bg_tilesets[ui.bg_tileset_list.currentItem().text()]
        self.unsaved_changes = True

    def delete_ob_tileset(self, ui):
        del self.ob_tilesets[ui.ob_tileset_list.currentItem().text()]
        self.unsaved_changes = True
