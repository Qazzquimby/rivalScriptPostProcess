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
        name = f"{remove_strip_length_from_name(sprite_name)}_offset"
        gml = _get_offset_gml(path)
        super().__init__(name, gml)


def _get_offset_gml(path):
    sprite_name = get_sprite_name(path)
    offsets = _calculate_offsets(path)
    return f"sprite_change_offset({remove_strip_length_from_name(sprite_name)}, {offsets[0]}, {offsets[1]});"


def _calculate_offsets(path: str) -> t.Tuple[int, int]:
    image = Image.open(path)
    height = image.height

    strip_width = image.width
    strip_frames = _get_frames_in_strip(path)
    width = strip_width / strip_frames

    # todo, height should be the distance from the top to the lowest pixel(?)

    return int(height // 2), int(width // 2)


def remove_strip_length_from_name(name):
    return name.split('_strip')[0]


def _get_frames_in_strip(path: str):
    try:
        length_str = path.split('strip')[-1].split('.png')[0]
        return int(length_str)
    except (IndexError, ValueError):
        return 1
