# This Python file uses the following encoding: utf-8

import os, json

from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

from map import Map
from tileset import Tileset

class Project:
    def __init__(self):
        self.name = None
        self.dir = None
        self.initialized = False
        self.unsaved_changes = False
        self.data = {}
        self.bg_tilesets = {}
        self.ob_tilesets = {}
        self.maps = {}

    def new(self, name, dir):
        self.name = name
        self.dir = dir
        self.initialized = True
        self.unsaved_changes = False
        os.makedirs(self.dir + "/tilesets/bg")
        os.makedirs(self.dir + "/tilesets/ob")
        os.makedirs(self.dir + "/maps")
        self.save()

    def load(self, ui, dir):
        data = json.loads(open(dir + "/project.json", "r").read())

        self.name = data["name"]
        self.dir = dir

        for name, filename in zip(data["bg_tilesets"]["names"], data["bg_tilesets"]["filenames"]):
            self.new_tileset("bg", name, filename)
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            ui.bg_tileset_list.addItem(item)

        for name, filename in zip(data["ob_tilesets"]["names"], data["ob_tilesets"]["filenames"]):
            self.new_tileset("ob", name, filename)
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            ui.ob_tileset_list.addItem(item)

        for name in data["maps"]:
            tileset = self.bg_tilesets[data["maps"][name]["tileset"]]
            self.maps[name] = Map(tileset, tilemap=data["maps"][name]["tilemap"])
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            ui.map_list.addItem(item)

        self.initialized = True
        self.unsaved_changes = False

    def save(self):
        data = {}

        data["name"] = self.name

        filenames = []
        for bg in self.bg_tilesets:
            filenames.append(self.bg_tilesets[bg].filename)
        data["bg_tilesets"] = {}
        data["bg_tilesets"]["names"] = list(self.bg_tilesets.keys())
        data["bg_tilesets"]["filenames"] = filenames

        filenames = []
        for ob in self.ob_tilesets:
            filenames.append(self.ob_tilesets[ob].filename)
        data["ob_tilesets"] = {}
        data["ob_tilesets"]["names"] = list(self.ob_tilesets.keys())
        data["ob_tilesets"]["filenames"] = filenames

        maps = {}
        for map in self.maps:
            maps[map] = self.maps[map].to_dict()
            for tileset in self.bg_tilesets:
                if self.bg_tilesets[tileset] == self.maps[map].tileset:
                    name = tileset
                    break
            maps[map]["tileset"] = name
        data["maps"] = maps

        open(self.dir + "/project.json", "w").write(json.dumps(data))
        self.unsaved_changes = False

    def compile(self):
        bin_files = {}
        inc_files = {}

        tilesets_string = ""
        bg_palettes_string = ""
        tilesets_bin = {}
        bg_palettes_bin = {}
        for tileset in self.bg_tilesets:
            tiledefs, palettes = self.bg_tilesets[tileset].to_bytearray()
            tilesets_bin[tileset] = tiledefs
            bg_palettes_bin[tileset] = palettes
            tilesets_string += "section \"tileset_" + tileset + "\", romx, align[4]\n"
            tilesets_string += "    incbin \"tilesets/" + tileset + ".bin\"\n\n"
            bg_palettes_string += "section \"bg_palettes_" + tileset + "\", romx\n"
            bg_palettes_string += "    incbin \"bg_palettes/" + tileset + ".bin\"\n\n"
        inc_files["tilesets"] = tilesets_string
        inc_files["bg_palettes"] = bg_palettes_string
        bin_files["tilesets"] = tilesets_bin
        bin_files["bg_palettes"] = bg_palettes_bin


        map_tiles_bin = {}
        map_attribs_bin = {}
        map_tiles_string = ""
        map_attribs_string = ""
        map_table_string = ""
        map_table_string += "if !def(MAPS_LOADED)\n"
        map_table_string += "    def MAPS_LOADED equ 1\n"
        map_table_string += "    include \"map_tiles.inc\"\n"
        map_table_string += "    include \"map_attribs.inc\"\n"
        map_table_string += "    include \"tilesets.inc\"\n"
        map_table_string += "    include \"bg_palettes.inc\"\n"
        map_table_string += "endc\n"
        map_table_string += "\n"
        map_table_string += "section \"map_table\", rom0\n"
        for map in self.maps:
            tile_ids, tile_attribs = self.maps[map].to_bytearray()
            map_tiles_bin[map] = tile_ids
            map_attribs_bin[map] = tile_attribs
            for tileset in self.bg_tilesets:
                if self.bg_tilesets[tileset] == self.maps[map].tileset:
                    tileset_name = tileset

            map_tiles_string += "section \"map_tiles_" + map + "\", romx, align[4]\n"
            map_tiles_string += "    incbin \"map_tiles/" + map + ".bin\"\n\n"

            map_attribs_string += "section \"map_attribs_" + map + "\", romx, align[4]\n"
            map_attribs_string += "    incbin \"map_attribs/" + map + ".bin\"\n\n"

            map_table_string += "    " + map + ":\n"

            map_table_string += "        " + "db " + str(self.maps[map].width()) + "\n"
            map_table_string += "        " + "db " + str(self.maps[map].height()) + "\n"
            map_table_string += "        " + "dw " + str(self.maps[map].width() * self.maps[map].height()) + "\n"

            map_table_string += "        " + "dw bank(\"map_tiles_" + map + "\")\n"
            map_table_string += "        " + "dw startof(\"map_tiles_" + map + "\")\n"

            map_table_string += "        " + "dw bank(\"map_attribs_" + map + "\")\n"
            map_table_string += "        " + "dw startof(\"map_attribs_" + map + "\")\n"

            map_table_string += "        " + "dw bank(\"tileset_" + tileset_name + "\")\n"
            map_table_string += "        " + "dw startof(\"tileset_" + tileset_name + "\")\n"

            map_table_string += "        " + "dw bank(\"bg_palettes_" + tileset_name + "\")\n"
            map_table_string += "        " + "dw startof(\"bg_palettes_" + tileset_name + "\")\n"

        inc_files["map_tiles"] = map_tiles_string
        inc_files["map_attribs"] = map_attribs_string
        inc_files["map_table"] = map_table_string
        bin_files["map_tiles"] = map_tiles_bin
        bin_files["map_attribs"] = map_attribs_bin

        os.makedirs(self.dir + "/out/inc", exist_ok=True)
        for filename, string in inc_files.items():
            with open(self.dir + "/out/inc/" + filename + ".inc", "w") as file:
                file.write(string)
        for folder in bin_files:
            os.makedirs(self.dir + "/out/bin/" + folder, exist_ok=True)
            for filename, bytes in bin_files[folder].items():
                with open(self.dir + "/out/bin/" + folder + "/" + filename + ".bin", "wb") as file:
                    file.write(bytes)

    def new_tileset(self, type, name, filename):
        if type == "bg":
            list = self.bg_tilesets
        elif type == "ob":
            list = self.ob_tilesets
        for tileset in list:
            if list[tileset].filename == filename:
                raise Exception("Tileset already loaded!")
        if name in list:
            raise Exception("Tileset with this name already loaded!")
        list[name] = Tileset(filename)
        self.unsaved_changes = True

    def rename_tileset(self, type, item):
        if type == "bg":
            lst = self.bg_tilesets
        elif type == "ob":
            lst = self.ob_tilesets
        new_name = item.text()
        old_items = lst.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        if new_name in old_items:
            item.setText(old_name)
            return
        lst[new_name] = lst[old_name]
        del lst[old_name]
        self.unsaved_changes = True

    def delete_tileset(self, type, name):
        if type == "bg":
            for map in self.maps:
                if self.maps[map].tileset == self.bg_tilesets[name]:
                    raise Exception("Cannot delete tileset: used in map '" + map + "'")
            del self.bg_tilesets[name]
        elif type == "ob":
            del self.ob_tilesets[name]
        self.unsaved_changes = True

    def new_map(self, name, tileset, width, height):
        if name in self.maps:
            raise Exception("Map with this name already exists!")
        self.maps[name] = Map(tileset, width, height)
        self.unsaved_changes = True

    def rename_map(self, item):
        new_name = item.text()
        old_items = self.maps.keys()
        old_name = list(set(old_items) - set([new_name]))[0]
        if new_name in old_items:
            item.setText(old_name)
            return
        self.maps[new_name] = self.maps[old_name]
        del self.maps[old_name]
        self.unsaved_changes = True

    def delete_map(self, name):
        del self.maps[name]
        self.unsaved_changes = True
