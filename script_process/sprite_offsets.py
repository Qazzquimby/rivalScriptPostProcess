import typing as t
import pathlib

from PIL import Image

from script_process.dependencies import GmlDependency


def get_sprite_paths(root_path):
    return f"{root_path}/sprites/*.png"


def load_gml_path(root_path):
    return f"{root_path}/scripts/load.gml"


def get_sprite_name(sprite_path):
    return pathlib.Path(sprite_path).stem


class SpriteOffsetDependency(GmlDependency):
    def __init__(self, path: str):
        sprite_name = get_sprite_name(path)
        name = f"{sprite_name}_offset"
        gml = self._get_offset_gml(path)
        super().__init__(name, gml)

    def _get_offset_gml(self, path):
        sprite_name = get_sprite_name(path)
        offsets = self._calculate_offsets(path)
        return f"sprite_change_offset({sprite_name}, {offsets[0]}, {offsets[1]});"

    def _calculate_offsets(self, path: str) -> t.Tuple[int, int]:
        # sprite_name = get_sprite_name(path)
        # todo make this work for sprite sheets

        image = Image.open(path)

        height = image.height

        strip_width = image.width

        return height // 2, strip_width // 2
