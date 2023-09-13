# This Python file uses the following encoding: utf-8

from tile import Tile
from tile_def import TileDef

class TileMap:
    def __init__(self, width, height):
        self.tiles = [[Tile() for j in range(0, height)] for i in range(0, width)]

    def __getitem__(self, idx):
        return self.tiles[idx]

    @classmethod
    def from_tileset(cls, tileset):
        tile_map = TileMap(tileset.pixmap.width() // 8, tileset.pixmap.height() // 8)
        for y in range(0, tileset.pixmap.height(), 8):
            for x in range(0, tileset.pixmap.width(), 8):
                tile_def = TileDef(tileset.pixmap.copy(x, y, 8, 8))
                for i in range(0, len(tileset.tile_defs)):
                    if tile_def == tileset.tile_defs[i]:
                        mirrored = tile_def.is_mirror(tileset.tile_defs[i])
                        palette = tile_def.get_palette()
                        for j in range(0, len(tileset.palettes)):
                            if all(color in tileset.palettes[j] for color in palette):
                                palette = j
                                break
                        tile_map[x // 8][y // 8] = Tile(i, palette, mirrored[0], mirrored[1])
                        break
        return tile_map
