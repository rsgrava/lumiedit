# This Python file uses the following encoding: utf-8

class Tile:
    def __init__(self, id=0, palette=0, flip_h=False, flip_v=False):
        self.id = id
        self.palette = palette
        self.flip_h = flip_h
        self.flip_v = flip_v
