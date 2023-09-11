# This Python file uses the following encoding: utf-8

import os

from tileset import Tileset

class Project:
    def __init__(self):
        self.bg_tilesets = {}
        self.ob_tilesets = {}

    def new(self, name):
        self.name = name

    def new_bg_tileset(self, filename):
        for tileset in self.bg_tilesets:
            if self.bg_tilesets[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        name = os.path.splitext(filename)[0].split('/')[-1]
        if name in self.bg_tilesets:
            raise Exception("Tileset with this name already loaded!")
        self.bg_tilesets[name] = Tileset(filename, "bg", True)

    def new_ob_tileset(self, filename):
        for tileset in self.ob_tilesets:
            if self.ob_tilesets[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        name = os.path.splitext(filename)[0].split('/')[-1]
        if name in self.ob_tilesets:
            raise Exception("Tileset with this name already loaded!")
        self.ob_tilesets[name] = Tileset(filename, "ob", False)

    def rename_bg_tileset(self, new_name):
        old_items = self.bg_tilesets.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        self.bg_tilesets[new_name] = self.bg_tilesets[old_name]
        del self.bg_tilesets[old_name]

    def rename_ob_tileset(self, new_name):
        old_items = self.ob_tilesets.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        self.ob_tilesets[new_name] = self.ob_tilesets[old_name]
        del self.ob_tilesets[old_name]
        print(self.ob_tilesets)
