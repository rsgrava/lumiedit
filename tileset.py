# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QPixmap

from tile_def import TileDef

class Tileset:
    def __init__(self, filename):
        self.filename = filename
        self.pixmap = QPixmap()
        ok = self.pixmap.load(filename)
        if not ok:
            raise Exception("Failed to load pixmap!")
        if self.pixmap.width() % 16 != 0 or self.pixmap.height() % 16 != 0:
            raise Exception("Invalid pixmap size!")

        self.tile_defs = []
        i = 0
        for y in range(0, self.pixmap.height(), 8):
            for x in range(0, self.pixmap.width(), 8):
                tile_def = TileDef(self.pixmap.copy(x, y, 8, 8))
                if tile_def not in self.tile_defs:
                    self.tile_defs.append(tile_def)
                if i > 256:
                    raise Exception("Too many tiles! (max 256)")
                i = i + 1

        self.palettes = []
        for tile in self.tile_defs:
            palette = tile.get_palette()
            if palette not in self.palettes:
                self.palettes.append(palette)
        subpalettes = []
        for i in range(0, len(self.palettes)):
            if len(self.palettes[i]) < 4:
                for j in range(0, len(self.palettes)):
                    if i == j:
                        continue
                    if all(color in self.palettes[j] for color in self.palettes[i]):
                        subpalettes.append(self.palettes[i])
        for subpalette in subpalettes:
            if subpalette in self.palettes:
                self.palettes.remove(subpalette)
        for palette in self.palettes:
            palette.pad()
        if len(self.palettes) > 8:
            raise Exception("More than 8 palettes in tileset!")
