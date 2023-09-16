# This Python file uses the following encoding: utf-8

from tiledef import Tiledef

class Tile:
    def __init__(self, id=0, palette=0, flip_h=False, flip_v=False):
        self.id = id
        self.palette = palette
        self.flip_h = flip_h
        self.flip_v = flip_v

    @classmethod
    def from_tileset(cls, tileset, x, y):
        tiledef = Tiledef(tileset.pixmap.copy(x, y, 8, 8))
        for i in range(0, len(tileset.tiledefs)):
            if tiledef == tileset.tiledefs[i]:
                mirrored = tiledef.is_mirror(tileset.tiledefs[i])
                palette = tiledef.get_palette()
                for j in range(0, len(tileset.palettes)):
                    if all(color in tileset.palettes[j] for color in palette):
                        palette = j
                        break
                return Tile(i, palette, mirrored[0], mirrored[1])

    @classmethod
    def from_dict(self, dct):
        return Tile(dct["id"], dct["palette"], dct["flip_h"], dct["flip_v"])

    def to_dict(self):
        return {
                   "id": self.id,
                   "palette": self.palette,
                   "flip_h": self.flip_h,
                   "flip_v": self.flip_v,
               }

    @classmethod
    def copy(cls, tile):
        return Tile(tile.id, tile.palette, tile.flip_h, tile.flip_v)
