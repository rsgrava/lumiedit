# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPixmap, QPen
from PySide6.QtCore import Qt

from tile import Tile

class MapEditor(QGraphicsScene):
    def __init__(self, tile_select, hflip_box, vflip_box):
        super().__init__()
        self.map = None
        self.mouse_held = False
        self.selection_rect = QGraphicsRectItem(0, 0, 64, 64)
        self.tile_select = tile_select
        self.hflip_box = hflip_box
        self.vflip_box = vflip_box

    def clear(self):
        super().clear()
        self.map = None
        self.clear_selection()

    def mouseMoveEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        if x <= 0 or x >= self.width() or y <= 0 or y >= self.height():
            self.clear_selection()
            self.mouse_held = False
            return
        self.set_selection(x // 64, y // 64)
        if self.mouse_held:
            self.write_metatile(x // 64, y // 64)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.clear_selection()
        self.mouse_held = False

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_held = False

    def mousePressEvent(self, event):
        if not self.map:
            return
        if event.button() == Qt.LeftButton:
            x = event.scenePos().x()
            y = event.scenePos().y()
            if x <= 0 or x >= self.width() or y <= 0 or y >= self.height():
                return
            self.write_metatile(x // 64, y // 64)
            self.mouse_held = True

    def write_metatile(self, metatile_x, metatile_y):
        tile_x = int(metatile_x * 2)
        tile_y = int(metatile_y * 2)
        metatile = self.tile_select.metatile

        tile0 = Tile.copy(metatile[0])
        tile1 = Tile.copy(metatile[1])
        tile2 = Tile.copy(metatile[2])
        tile3 = Tile.copy(metatile[3])

        flip_h = self.hflip_box.isChecked()
        flip_v = self.vflip_box.isChecked()
        tile0.flip_h = metatile[0].flip_h != flip_h
        tile0.flip_v = metatile[0].flip_v != flip_v
        tile1.flip_h = metatile[1].flip_h != flip_h
        tile1.flip_v = metatile[1].flip_v != flip_v
        tile2.flip_h = metatile[2].flip_h != flip_h
        tile2.flip_v = metatile[2].flip_v != flip_v
        tile3.flip_h = metatile[3].flip_h != flip_h
        tile3.flip_v = metatile[3].flip_v != flip_v

        match (flip_h, flip_v):
            case (False, False):
                self.map[tile_x][tile_y] = tile0
                self.map[tile_x + 1][tile_y] = tile1
                self.map[tile_x][tile_y + 1] = tile2
                self.map[tile_x + 1][tile_y + 1] = tile3
            case (True, False):
                self.map[tile_x + 1][tile_y] = tile0
                self.map[tile_x][tile_y] = tile1
                self.map[tile_x + 1][tile_y + 1] = tile2
                self.map[tile_x][tile_y + 1] = tile3
            case (False, True):
                self.map[tile_x][tile_y + 1] = tile0
                self.map[tile_x + 1][tile_y + 1] = tile1
                self.map[tile_x][tile_y] = tile2
                self.map[tile_x + 1][tile_y] = tile3
            case (True, True):
                self.map[tile_x + 1][tile_y + 1] = tile0
                self.map[tile_x][tile_y + 1] = tile1
                self.map[tile_x + 1][tile_y] = tile2
                self.map[tile_x][tile_y] = tile3

        super().clear()
        self.draw_map()
        self.set_selection(metatile_x, metatile_y)

    def set_selection(self, metatile_x, metatile_y):
        self.clear_selection()
        pen = QPen("red")
        pen.setWidth(4)
        self.selection_rect.setPen(pen)
        self.addItem(self.selection_rect)
        self.selection_rect.setPos(metatile_x * 64, metatile_y * 64)

    def clear_selection(self):
        if self.selection_rect in self.items():
            self.removeItem(self.selection_rect)
        self.selection_rect = QGraphicsRectItem(0, 0, 64, 64)

    def set_map(self, map):
        self.map = map
        self.refresh()

    def draw_map(self):
        self.setSceneRect(0, 0, self.map.width() * 32, self.map.height() * 32)
        for tile_y in range(0, self.map.tilemap.height()):
            for tile_x in range(0, self.map.tilemap.width()):
                tile = self.map.tilemap[tile_x][tile_y]
                tiledef = self.map.tileset[tile.id]
                x = tile_x * 32
                y = tile_y * 32
                item = self.addPixmap(QPixmap.fromImage(tiledef.pixmap.toImage().mirrored(tile.flip_h, tile.flip_v)))
                item.setPos(x, y)
                item.setScale(4)

    def refresh(self):
        if self.map:
            super().clear()
            self.draw_map()
