# This Python file uses the following encoding: utf-8

from tile import Tile
from tiledef import Tiledef

class Tilemap:
    def __init__(self, width, height, default_metatile=None):
        self.tiles = [[Tile() for j in range(0, height)] for i in range(0, width)]
        if default_metatile:
            for x in range(0, len(self.tiles), 2):
                for y in range(0, len(self.tiles), 2):
                    self.tiles[x][y] = Tile.copy(default_metatile[0])
                    self.tiles[x + 1][y] = Tile.copy(default_metatile[1])
                    self.tiles[x][y + 1] = Tile.copy(default_metatile[2])
                    self.tiles[x + 1][y + 1] = Tile.copy(default_metatile[3])


    def __getitem__(self, idx):
        return self.tiles[idx]

    def width(self):
        return len(self.tiles)

    def height(self):
        return len(self.tiles[0])

    @classmethod
    def from_tileset(cls, tileset):
        tilemap = Tilemap(tileset.pixmap.width() // 8, tileset.pixmap.height() // 8)
        for y in range(0, tileset.pixmap.height(), 8):
            for x in range(0, tileset.pixmap.width(), 8):
                tilemap[x // 8][y // 8] = Tile.from_tileset(tileset, x, y)
        return tilemap
