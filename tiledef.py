# This Python file uses the following encoding: utf-8

from palette import Palette

class Tiledef:
    def __init__(self, pixmap):
        self.pixmap = pixmap

    def __eq__(self, other):
        mirrored = self.is_mirror(other)
        return self.pixmap.toImage() == other.pixmap.toImage() or mirrored[0] or mirrored[1]

    def to_bytearray(self, palette):
        image = self.pixmap.toImage()
        bytes = bytearray()
        pixel_ids = []
        for y in range(0, self.pixmap.width()):
            for x in range(0, self.pixmap.height()):
                color = image.pixelColor(x, y)
                for i in range(0, len(palette)):
                    if palette[i] == color:
                        pixel_ids.append(i)
                        break
        for row in range(0, 8):
            lo_byte = 0
            hi_byte = 0
            ids = pixel_ids[row * 8:row * 8 + 8]
            for id in ids:
                lo_byte <<= 1
                hi_byte <<= 1
                lo_byte |= id % 2
                hi_byte |= id // 2
            bytes.append(lo_byte)
            bytes.append(hi_byte)
        return bytes

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
