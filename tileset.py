# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QPixmap

from tile import Tile
from tiledef import Tiledef

class Tileset:
    def __init__(self, filename):
        self.filename = filename
        self.pixmap = QPixmap()
        ok = self.pixmap.load(filename)
        if not ok:
            raise Exception("Failed to load pixmap!")
        if self.pixmap.width() % 16 != 0 or self.pixmap.height() % 16 != 0:
            raise Exception("Invalid pixmap size!")

        self.tiledefs = []
        i = 0
        for y in range(0, self.pixmap.height(), 8):
            for x in range(0, self.pixmap.width(), 8):
                tiledef = Tiledef(self.pixmap.copy(x, y, 8, 8))
                if tiledef not in self.tiledefs:
                    self.tiledefs.append(tiledef)
                    i = i + 1
                if i > 384:
                    raise Exception("Too many tiles! (max 384)")

        self.palettes = []
        for tile in self.tiledefs:
            palette = tile.get_palette()
            if palette not in self.palettes:
                self.palettes.append(palette)
        subpalettes = []
        for i in range(0, len(self.palettes)):
            if len(self.palettes[i]) < 4:
                for j in range(0, len(self.palettes)):
                    if i == j:
                        continue
                    if self.palettes[i].is_subpalette(self.palettes[j]):
                        subpalettes.append(self.palettes[i])
        for subpalette in subpalettes:
            if subpalette in self.palettes:
                self.palettes.remove(subpalette)
        for palette in self.palettes:
            palette.pad()
        if len(self.palettes) > 8:
            raise Exception("More than 8 palettes in tileset!")

        self.def_palettes = []
        for tiledef in self.tiledefs:
            palette = tiledef.get_palette()
            for other in self.palettes:
                if palette.is_subpalette(other):
                    self.def_palettes.append(other)
                    break

    def __getitem__(self, id):
        return self.tiledefs[id]

    def first_metatile(self):
        first_metatile = []
        for y in range(0, 16, 8):
            for x in range(0, 16, 8):
                first_metatile.append(Tile.from_tileset(self, x, y))
        return first_metatile

    def to_bytearray(self):
        tiledefs = bytearray()
        for tiledef, palette in zip(self.tiledefs, self.def_palettes):
            tiledefs += tiledef.to_bytearray(palette)
        palettes = bytearray()
        for palette in self.palettes:
            palettes += palette.to_bytearray()
        palettes = palettes + bytearray([0] * (64 - len(palettes)))
        return tiledefs, palettes
