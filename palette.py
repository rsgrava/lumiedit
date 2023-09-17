# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QColor

class Palette:
    def __init__(self):
        self.rgb = []
        self.gb = []

    def __contains__(self, color):
        return rgb_to_gb(color) in self.gb

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(color in other.gb for color in self.gb)

    def __getitem__(self, idx):
        return self.rgb[idx]

    def __len__(self):
        return len(self.rgb)

    def is_subpalette(self, other):
        return all(color in other for color in self)

    def to_bytearray(self):
        bytes = bytearray()
        for color in self.gb:
            color_bytes = color[0] | color[1] << 5 | color[2] << 10
            bytes.append(color_bytes & 0xFF)
            bytes.append(color_bytes >> 8)
        return bytes

    def append(self, color):
        self.rgb.append(color)
        self.gb.append(rgb_to_gb(color))

    def sort(self):
        def rgb_to_luma(color):
            if color.alpha() == 0:
                return 100000000
            return 0.2126 * color.red() + 0.7152 * color.green() + 0.0722 * color.blue()
        def gb_to_luma(color):
            if color[3] == 0:
                return 100000000
            return 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        self.rgb.sort(key=lambda x: rgb_to_luma(x), reverse=True)
        self.gb.sort(key=lambda x: gb_to_luma(x), reverse=True)

    def pad(self):
        while len(self.rgb) < 4:
            self.rgb.insert(0, QColor(0, 0, 0, 0))
            self.gb.insert(0, (0, 0, 0, 0))

def rgb_to_gb(color):
    red = color.red() >> 3
    green = color.green() >> 3
    blue = color.blue() >> 3
    alpha = color.alpha() >> 3
    return (red, green, blue, alpha)
