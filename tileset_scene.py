# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPen, QPixmap
from PySide6.QtCore import Qt

from tilemap import Tilemap

class TilesetScene(QGraphicsScene):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.clear()

    def clear(self):
        super().clear()
        self.tileset = None
        pen = QPen("red")
        pen.setWidth(4)
        self.selection_rect = QGraphicsRectItem(0, 0, 32, 32)
        self.selection_rect.setPen(pen)
        self.rect_spawned = False
        self.ui.tile_view.scene().clear()
        self.ui.palette_view.scene().clear()
        self.ui.palette0_view.scene().clear()
        self.ui.palette1_view.scene().clear()
        self.ui.palette2_view.scene().clear()
        self.ui.palette3_view.scene().clear()
        self.ui.palette4_view.scene().clear()
        self.ui.palette5_view.scene().clear()
        self.ui.palette6_view.scene().clear()
        self.ui.palette7_view.scene().clear()
        self.ui.metatile_label.setText("Metatile: -")
        self.ui.tile_label.setText("Tile: -")
        self.ui.palette_label.setText("Palette: -")
        self.ui.fliph_label.setText("Flip Hor: -")
        self.ui.flipv_label.setText("Flip Ver: -")

    def mousePressEvent(self, event):
        if not self.tileset:
            return
        if event.button() == Qt.LeftButton:
            tile_x = int(event.scenePos().x() // 32)
            tile_y = int(event.scenePos().y() // 32)
            x = tile_x * 32
            y = tile_y * 32
            if x < 0 or y < 0 or x > (self.width() - 32) or (y > self.height() - 32):
                return

            if not self.rect_spawned:
                self.addItem(self.selection_rect)
                self.rect_spawned = True
            self.selection_rect.setPos(x, y)

            if self.ui.palette_view.scene() == None:
                self.ui.palette_view.setScene(QGraphicsScene(0, 0, 128, 32))

            self.ui.tile_view.scene().clear()
            self.ui.palette_view.scene().clear()

            tile = self.tilemap[tile_x][tile_y]

            self.ui.metatile_label.setText("Metatile: " + str(tile_y // 2 * (self.tileset.pixmap.width() // 16) + tile_x // 2))
            self.ui.tile_label.setText("Tile: " + str(tile.id))
            self.ui.palette_label.setText("Palette: " + str(tile.palette))
            self.ui.fliph_label.setText("Flip Hor: " + str(tile.flip_h))
            self.ui.flipv_label.setText("Flip Ver: " + str(tile.flip_v))

            tile_def = self.tileset.tile_defs[tile.id]
            pixmap = QPixmap.fromImage(tile_def.pixmap.toImage().mirrored(tile.flip_h, tile.flip_v))
            item = self.ui.tile_view.scene().addPixmap(pixmap)
            item.setScale(8)

            palette = self.tileset.palettes[tile.palette]
            self.ui.palette_view.set_palette(palette)

    def setTileset(self, tileset):
        self.tileset = tileset
        self.tilemap = Tilemap.from_tileset(tileset)
        self.setSceneRect(0, 0, tileset.pixmap.width() * 4, tileset.pixmap.height() * 4)
        item = self.addPixmap(tileset.pixmap)
        item.setScale(4)
        for y in range(0, tileset.pixmap.height() * 4, 64):
            for x in range(0, tileset.pixmap.width() * 4, 64):
                self.addRect(x, y, 64, 64)
        self.ui.palette0_view.set_palette(tileset.palettes[0])
        if len(tileset.palettes) > 1:
            self.ui.palette1_view.set_palette(tileset.palettes[1])
        if len(tileset.palettes) > 2:
            self.ui.palette2_view.set_palette(tileset.palettes[2])
        if len(tileset.palettes) > 3:
            self.ui.palette3_view.set_palette(tileset.palettes[3])
        if len(tileset.palettes) > 4:
            self.ui.palette4_view.set_palette(tileset.palettes[4])
        if len(tileset.palettes) > 5:
            self.ui.palette5_view.set_palette(tileset.palettes[5])
        if len(tileset.palettes) > 6:
            self.ui.palette6_view.set_palette(tileset.palettes[6])
        if len(tileset.palettes) > 7:
            self.ui.palette7_view.set_palette(tileset.palettes[7])
