# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QColor

class Tile:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def get_palettes(self):
        palettes = []
        subtiles = []
        subtiles.append(self.get_subtile(0))
        subtiles.append(self.get_subtile(1))
        subtiles.append(self.get_subtile(2))
        subtiles.append(self.get_subtile(3))
        for subtile in subtiles:
            palette = get_subtile_palette(subtile)
            if ele_not_in_list(palette, palettes):
                palettes.append(palette)
        return palettes

    def get_subtile(self, idx):
        match idx:
            case 0:
                return self.image.copy(0, 0, 8, 8).toImage()
            case 1:
                return self.image.copy(8, 0, 8, 8).toImage()
            case 2:
                return self.image.copy(0, 8, 8, 8).toImage()
            case 3:
                return self.image.copy(8, 8, 8, 8).toImage()


def get_subtile_palette(subtile):
    palette = []
    for y in range(0, 8):
        for x in range(0, 8):
            color = subtile.pixelColor(x, y)
            if ele_not_in_list(color, palette):
                palette.append(color)
    if len(palette) > 4:
        raise Exception("Tile palette with more than 4 colors!")
    palette.sort(key=lambda x: rgb_to_luma(x), reverse=True)
    return palette


def ele_not_in_list(color, palette):
    for other in palette:
        if color == other:
            return False
    return True

def rgb_to_luma(color):
    if color.alpha() == 0:
        return 100000000
    return 0.2126 * color.red() + 0.7152 * color.green() + 0.0722 * color.blue()
