# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPixmap, QPen, QBrush
from PySide6.QtCore import Qt

class TilesetScene(QGraphicsScene):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.tileset = None
        self.set_rect()

    def set_rect(self):
        pen = QPen("red")
        pen.setWidth(4)
        self.selection_rect = QGraphicsRectItem(0, 0, 32, 32)
        self.selection_rect.setPen(pen)
        self.rect_spawned = False

    def mousePressEvent(self, event):
        if not self.tileset:
            return
        if event.button() == Qt.LeftButton:
            subtile_x = event.scenePos().x() // 32
            subtile_y = event.scenePos().y() // 32
            x = subtile_x * 32
            y = subtile_y * 32

            if x < 0 or y < 0 or x > (self.width() - 32) or (y > self.height() - 32):
                return

            if not self.rect_spawned:
                self.addItem(self.selection_rect)
                self.rect_spawned = True
            self.selection_rect.setPos(x, y)

            if self.ui.palette_view.scene() == None:
                self.ui.palette_view.setScene(QGraphicsScene(0, 0, 128, 32))

            self.ui.subtile_view.scene().clear()
            self.ui.palette_view.scene().clear()

            subtile = self.tileset.get_subtile(subtile_x, subtile_y)
            subtile_idx = self.tileset.get_subtile_idx(subtile_x, subtile_y)
            tile_idx = self.tileset.get_tile_idx(subtile_x // 2, subtile_y // 2)
            palette_idx = self.tileset.get_subtile_palette_idx(subtile_x, subtile_y)
            palette = self.tileset.palettes[palette_idx]

            self.ui.tile_label.setText("Tile: " + str(tile_idx))
            self.ui.subtile_label.setText("Subtile: " + str(subtile_idx))
            self.ui.palette_label.setText("Palette: " + str(palette_idx))

            item = self.ui.subtile_view.scene().addPixmap(QPixmap.fromImage(subtile))
            item.setScale(8)

            brush = QBrush(palette[0])
            self.ui.palette_view.scene().addRect(0, 0, 32, 32, brush=brush)
            brush.setColor(palette[1])
            self.ui.palette_view.scene().addRect(32, 0, 32, 32, brush=brush)
            brush.setColor(palette[2])
            self.ui.palette_view.scene().addRect(64, 0, 32, 32, brush=brush)
            brush.setColor(palette[3])
            self.ui.palette_view.scene().addRect(96, 0, 32, 32, brush=brush)
