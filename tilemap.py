# This Python file uses the following encoding: utf-8

from tile import Tile
from tiledef import Tiledef

class Tilemap:
    def __init__(self, width, height):
        self.tiles = [[Tile() for j in range(0, height)] for i in range(0, width)]

    def __getitem__(self, idx):
        return self.tiles[idx]

    @classmethod
    def from_tileset(cls, tileset):
        tilemap = Tilemap(tileset.pixmap.width() // 8, tileset.pixmap.height() // 8)
        for y in range(0, tileset.pixmap.height(), 8):
            for x in range(0, tileset.pixmap.width(), 8):
                tiledef = Tiledef(tileset.pixmap.copy(x, y, 8, 8))
                for i in range(0, len(tileset.tiledefs)):
                    if tiledef == tileset.tiledefs[i]:
                        mirrored = tiledef.is_mirror(tileset.tiledefs[i])
                        palette = tiledef.get_palette()
                        for j in range(0, len(tileset.palettes)):
                            if all(color in tileset.palettes[j] for color in palette):
                                palette = j
                                break
                        tilemap[x // 8][y // 8] = Tile(i, palette, mirrored[0], mirrored[1])
                        break
        return tilemap
