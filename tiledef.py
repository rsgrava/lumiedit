# This Python file uses the following encoding: utf-8

from palette import Palette

class Tiledef:
    def __init__(self, pixmap):
        self.pixmap = pixmap

    def __eq__(self, other):
        mirrored = self.is_mirror(other)
        return self.pixmap.toImage() == other.pixmap.toImage() or mirrored[0] or mirrored[1]

    def is_mirror(self, other):
        image1 = self.pixmap.toImage()
        image2 = other.pixmap.toImage()
        if image1 == image2.mirrored(True, True):
            return (True, True)
        elif image1 == image2.mirrored(True, False):
            return (True, False)
        elif image1 == image2.mirrored(False, True):
            return (False, True)
        return (False, False)

    def get_palette(self):
        image = self.pixmap.toImage()
        palette = Palette()
        for y in range(0, 8):
            for x in range(0, 8):
                color = image.pixelColor(x, y)
                if color not in palette:
                    palette.append(color)
        palette.sort()
        return palette
