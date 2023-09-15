# This Python file uses the following encoding: utf-8

from tilemap import Tilemap

class Map:
    def __init__(self, tileset, width, height):
        self.tileset = tileset
        self.tilemap = Tilemap(width * 2, height * 2, tileset.first_metatile())

    def __getitem__(self, idx):
        return self.tilemap[idx]

    def width(self):
        return len(self.tilemap.tiles)

    def height(self):
        return len(self.tilemap.tiles[0])
