# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPen, QPixmap, QPainter, QColor, QBrush
from PySide6.QtCore import Qt

from tilemap import Tilemap

class TileSelectScene(QGraphicsScene):
    def __init__(self, hflip_box, vflip_box):
        super().__init__()
        self.hflip_box = hflip_box
        self.vflip_box = vflip_box
        self.clear()

    def clear(self):
        super().clear()
        self.selection_rect = QGraphicsRectItem(0, 0, 64, 64)
        self.tileset = None
        self.metatile_idx = 0
        self.metatiles = []
        self.metatile = None

    def mousePressEvent(self, event):
        if not self.tileset:
            return
        if event.button() == Qt.LeftButton:
            metatile_x = int(event.scenePos().x() // 64)
            metatile_y = int(event.scenePos().y() // 64)
            x = metatile_x * 64
            y = metatile_y * 64
            if (x < 0 or y < 0 or x > (self.width() - 64) or (y > self.height() - 64) or
               (metatile_y == self.metatiles_y - 1 and
                self.metatiles_last_line != 0 and metatile_x > self.metatiles_last_line - 1)):
                return
            self.metatile_idx = metatile_x + self.metatiles_x * metatile_y
            self.metatile = self.metatiles[self.metatile_idx]
            self.set_selection(self.metatile_idx)

    def setTileset(self, tileset):
        self.tileset = tileset
        self.tilemap = Tilemap.from_tileset(tileset)
        self.draw_pixmap()
        self.set_selection(0)

    def draw_pixmap(self):
        view_width = self.views()[0].width()
        num_metatiles = (self.tileset.pixmap.width() // 16) * (self.tileset.pixmap.height() // 16)
        self.metatiles_x = view_width // 64
        self.metatiles_last_line = num_metatiles % self.metatiles_x
        self.metatiles_y = num_metatiles // self.metatiles_x + (1 if self.metatiles_last_line != 0 else 0)
        width = int(self.metatiles_x * 16)
        height = int(self.metatiles_y * 16)
        self.setSceneRect(0, 0, view_width - view_width % 64, height * 4)

        self.metatiles = []
        for y in range(0, self.tilemap.height(), 2):
            for x in range(0, self.tilemap.width(), 2):
                metatile = []
                metatile.append(self.tilemap[x][y])
                metatile.append(self.tilemap[x + 1][y])
                metatile.append(self.tilemap[x][y + 1])
                metatile.append(self.tilemap[x + 1][y + 1])
                self.metatiles.append(metatile)

        pixmap = QPixmap(width * 4, height * 4)
        painter = QPainter(pixmap)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRect(0, 0, self.views()[0].width(), self.views()[0].height())
        metatile_idx = 0
        for y in range(0, height, 16):
            for x in range(0, width, 16):
                if metatile_idx == num_metatiles:
                    break
                metatile = self.metatiles[metatile_idx]
                flip_h = self.hflip_box.isChecked()
                flip_v = self.vflip_box.isChecked()
                tile0 = self.tileset[metatile[0].id].pixmap.toImage()
                tile1 = self.tileset[metatile[1].id].pixmap.toImage()
                tile2 = self.tileset[metatile[2].id].pixmap.toImage()
                tile3 = self.tileset[metatile[3].id].pixmap.toImage()
                tile0 = QPixmap.fromImage(tile0.mirrored(flip_h != metatile[0].flip_h, flip_v != metatile[0].flip_v))
                tile1 = QPixmap.fromImage(tile1.mirrored(flip_h != metatile[1].flip_h, flip_v != metatile[1].flip_v))
                tile2 = QPixmap.fromImage(tile2.mirrored(flip_h != metatile[2].flip_h, flip_v != metatile[2].flip_v))
                tile3 = QPixmap.fromImage(tile3.mirrored(flip_h != metatile[3].flip_h, flip_v != metatile[3].flip_v))
                match (self.hflip_box.isChecked(), self.vflip_box.isChecked()):
                    case (False, False):
                        painter.drawPixmap(x, y, tile0)
                        painter.drawPixmap(x + 8, y, tile1)
                        painter.drawPixmap(x, y + 8, tile2)
                        painter.drawPixmap(x + 8, y + 8, tile3)
                    case(True, False):
                        painter.drawPixmap(x + 8, y, tile0)
                        painter.drawPixmap(x, y, tile1)
                        painter.drawPixmap(x + 8, y + 8, tile2)
                        painter.drawPixmap(x, y + 8, tile3)
                    case(False, True):
                        painter.drawPixmap(x, y + 8, tile0)
                        painter.drawPixmap(x + 8, y + 8, tile1)
                        painter.drawPixmap(x, y, tile2)
                        painter.drawPixmap(x + 8, y, tile3)
                    case(True, True):
                        painter.drawPixmap(x + 8, y + 8, tile0)
                        painter.drawPixmap(x, y + 8, tile1)
                        painter.drawPixmap(x + 8, y, tile2)
                        painter.drawPixmap(x, y, tile3)
                metatile_idx = metatile_idx + 1
        painter.end()
        item = self.addPixmap(pixmap)
        item.setScale(4)
        self.metatile = self.metatiles[self.metatile_idx]

        metatile_idx = 0
        for y in range(0, height * 4, 64):
            for x in range(0, width * 4, 64):
                if metatile_idx == num_metatiles:
                    break
                self.addRect(x, y, 64, 64)
                metatile_idx = metatile_idx + 1

    def set_selection(self, metatile_idx):
        if self.selection_rect in self.items():
            self.removeItem(self.selection_rect)
        x = (metatile_idx % self.metatiles_x) * 64
        y = (metatile_idx // self.metatiles_x) * 64
        pen = QPen("red")
        pen.setWidth(4)
        self.selection_rect = QGraphicsRectItem(x, y, 64, 64)
        self.selection_rect.setPen(pen)
        self.addItem(self.selection_rect)

    def refresh(self):
        if self.tileset:
            self.draw_pixmap()
            self.set_selection(self.metatile_idx)
