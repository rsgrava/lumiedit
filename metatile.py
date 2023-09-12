# This Python file uses the following encoding: utf-8

from palette import Palette

class MetaTile:
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
            if palette not in palettes:
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
    palette = Palette()
    for y in range(0, 8):
        for x in range(0, 8):
            color = subtile.pixelColor(x, y)
            if color not in palette:
                palette.append(color)
    palette.sort()
    return palette
