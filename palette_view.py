# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QBrush

class PaletteView(QGraphicsView):
    def __init__(self, tilesets_tab):
        super().__init__(tilesets_tab)
        self.setScene(QGraphicsScene(0, 0, 128, 32))

    def set_palette(self, palette):
        brush = QBrush(palette[0])
        self.scene().addRect(0, 0, 32, 32, brush=brush)
        brush.setColor(palette[1])
        self.scene().addRect(32, 0, 32, 32, brush=brush)
        brush.setColor(palette[2])
        self.scene().addRect(64, 0, 32, 32, brush=brush)
        brush.setColor(palette[3])
        self.scene().addRect(96, 0, 32, 32, brush=brush)
