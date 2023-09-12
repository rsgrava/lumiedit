# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QPixmap, QColor

from tile import Tile, get_subtile_palette

class Tileset:
    def __init__(self, filename, type, padding):
        self.filename = filename
        self.tiles = []
        self.palettes = []

        image = QPixmap()
        ok = image.load(filename)
        if not ok:
            raise Exception("Failed to load image!")

        self.width = image.width()
        self.height = image.height()
        self.tile_width = self.width // 16
        if self.width % 16 != 0 or self.height % 16 != 0:
            raise Exception("Invalid image size!")

        i = 0
        for y in range(0, image.height(), 16):
            for x in range(0, image.width(), 16):
                self.tiles.append(Tile(image.copy(x, y, 16, 16), x, y))
                if i > 64:
                    raise Exception("Too many tiles! (max 64)")
                i = i + 1

        for tile in self.tiles:
            for palette in tile.get_palettes():
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

    def get_tile_idx(self, tile_x, tile_y):
        return int(tile_y * self.tile_width + tile_x)

    def get_subtile_idx(self, subtile_x, subtile_y):
        return int(subtile_x % 2 + 2 * (subtile_y % 2))

    def get_subtile(self, subtile_x, subtile_y):
        tile = self.tiles[self.get_tile_idx(subtile_x // 2, subtile_y // 2)]
        return tile.get_subtile(self.get_subtile_idx(subtile_x, subtile_y))

    def get_subtile_palette_idx(self, subtile_x, subtile_y):
        subtile = self.get_subtile(subtile_x, subtile_y)
        palette = get_subtile_palette(subtile)
        for i in range(0, len(self.palettes)):
            if all(color in self.palettes[i] for color in palette):
                return i
