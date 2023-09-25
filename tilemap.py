# This Python file uses the following encoding: utf-8

from tile import Tile

class Tilemap:
    def __init__(self, width, height, default_metatile=None):
        self.tiles = [[Tile() for j in range(0, height)] for i in range(0, width)]
        if default_metatile:
            for x in range(0, width, 2):
                for y in range(0, height, 2):
                    self.tiles[x][y] = Tile.copy(default_metatile[0])
                    self.tiles[x + 1][y] = Tile.copy(default_metatile[1])
                    self.tiles[x][y + 1] = Tile.copy(default_metatile[2])
                    self.tiles[x + 1][y + 1] = Tile.copy(default_metatile[3])

    def __getitem__(self, idx):
        return self.tiles[idx]

    @classmethod
    def from_tileset(cls, tileset):
        tilemap = Tilemap(tileset.pixmap.width() // 8, tileset.pixmap.height() // 8)
        for y in range(0, tileset.pixmap.height(), 8):
            for x in range(0, tileset.pixmap.width(), 8):
                tilemap[x // 8][y // 8] = Tile.from_tileset(tileset, x, y)
        return tilemap

    @classmethod
    def from_list(cls, lst):
        tilemap = Tilemap(len(lst), len(lst[0]))
        for x in range(0, len(lst)):
            for y in range(0, len(lst[x])):
                tilemap[x][y] = Tile.from_dict(lst[x][y])
        return tilemap

    def to_bytearray(self):
        ids = bytearray()
        attribs = bytearray()
        for y in range(0, self.height()):
            for x in range(0, self.width()):
                tile = self.tiles[x][y]
                attrib = 0
                attrib |= tile.palette
                attrib |= 0x20 if tile.flip_h else 0x00
                attrib |= 0x40 if tile.flip_v else 0x00
                attrib |= 0x08 if tile.id >= 256 else 0x00
                ids.append(tile.id if tile.id < 256 else tile.id - 256)
                attribs.append(attrib)
        return ids, attribs

    def to_dict(self):
        tiles = []
        for x in range(0, len(self.tiles)):
            col = []
            for y in range(0, len(self.tiles[x])):
                col.append(self.tiles[x][y].to_dict())
            tiles.append(col)
        return tiles

    def width(self):
        return len(self.tiles)

    def height(self):
        return len(self.tiles[0])
