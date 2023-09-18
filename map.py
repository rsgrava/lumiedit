# This Python file uses the following encoding: utf-8

from tilemap import Tilemap

class Map:
    def __init__(self, tileset, width=10, height=8, tilemap=None):
        self.tileset = tileset
        if tilemap == None:
            self.tilemap = Tilemap(width * 2, height * 2, tileset.first_metatile())
        else:
            self.tilemap = Tilemap.from_list(tilemap)

    def __getitem__(self, idx):
        return self.tilemap[idx]

    def to_bytearray(self):
        return self.tilemap.to_bytearray()

    def to_dict(self):
        return {
                    "tilemap": self.tilemap.to_dict(),
               }

    def width(self):
        return len(self.tilemap.tiles)

    def height(self):
        return len(self.tilemap.tiles[0])
