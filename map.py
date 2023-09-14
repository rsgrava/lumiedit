# This Python file uses the following encoding: utf-8

from tilemap import Tilemap

class Map:
    def __init__(self, tileset, width, height):
        self.tileset = tileset
        self.tilemap = Tilemap(width, height)
