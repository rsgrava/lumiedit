# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPen, QPixmap, QPainter, QColor, QBrush
from PySide6.QtCore import Qt

from tilemap import Tilemap

class TileSelectScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.clear()

    def clear(self):
        super().clear()
        self.tileset = None

    def mousePressEvent(self, event):
        if not self.tileset:
            return
        if event.button() == Qt.LeftButton:
            metatile_x = int(event.scenePos().x() // 64)
            metatile_y = int(event.scenePos().y() // 64)
            x = metatile_x * 64
            y = metatile_y * 64
            if (x < 0 or y < 0 or x > (self.width() - 64) or (y > self.height() - 64) or
               (metatile_y == self.metatiles_y - 1 and metatile_x > self.metatiles_last_line - 1)):
                return
            self.selection_rect.setPos(x, y)
            self.metatile = self.metatiles[metatile_x + self.metatiles_x  * metatile_y]

    def setTileset(self, tileset, view_width):
        self.tileset = tileset
        self.tilemap = Tilemap.from_tileset(tileset)
        self.draw_pixmap(view_width)
        pen = QPen("red")
        pen.setWidth(4)
        self.selection_rect = QGraphicsRectItem(0, 0, 64, 64)
        self.selection_rect.setPen(pen)
        self.addItem(self.selection_rect)

    def draw_pixmap(self, view_width):
        num_metatiles = (self.tileset.pixmap.width() // 16) * (self.tileset.pixmap.height() // 16)
        self.metatiles_x = view_width // 64
        self.metatiles_last_line = num_metatiles % self.metatiles_x
        self.metatiles_y = num_metatiles // self.metatiles_x + (1 if self.metatiles_last_line != 0 else 0)
        width = int(self.metatiles_x * 16)
        height = int(self.metatiles_y * 16)
        self.setSceneRect(0, 0, view_width - view_width % 64, height * 4)

        self.metatiles = []
        for y in range(0, len(self.tilemap), 2):
            for x in range(0, len(self.tilemap[y]), 2):
                metatile = []
                metatile.append(self.tilemap[x][y])
                metatile.append(self.tilemap[x + 1][y])
                metatile.append(self.tilemap[x][y + 1])
                metatile.append(self.tilemap[x + 1][y + 1])
                self.metatiles.append(metatile)

        pixmap = QPixmap(width * 4, height * 4)
        painter = QPainter(pixmap)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRect(0, 0, self.width(), self.height())
        metatile_idx = 0
        for y in range(0, height, 16):
            for x in range(0, width, 16):
                if metatile_idx == num_metatiles:
                    break
                metatile = self.metatiles[metatile_idx]
                painter.drawPixmap(x, y, self.tileset[metatile[0].id].pixmap)
                painter.drawPixmap(x + 8, y, self.tileset[metatile[1].id].pixmap)
                painter.drawPixmap(x, y + 8, self.tileset[metatile[2].id].pixmap)
                painter.drawPixmap(x + 8, y + 8, self.tileset[metatile[3].id].pixmap)
                metatile_idx = metatile_idx + 1
        painter.end()
        item = self.addPixmap(pixmap)
        item.setScale(4)

        for y in range(0, height * 4, 64):
            for x in range(0, width * 4, 64):
                if metatile_idx == num_metatiles:
                    break
                self.addRect(x, y, 64, 64)
                metatile_idx = metatile_idx + 1

    def resizeEvent(self, event):
        ...

    def mirror_h(self):
        ...

    def mirror_v(self):
        ...
