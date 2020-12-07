import pathlib
import glob


def get_root_path(path: str):
    try:
        return current_path_or_parent(pathlib.Path(path))
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't find the root directory")


def current_path_or_parent(path: pathlib.Path):
    subfolder_names = [pathlib.Path(subfolder).name
                       for subfolder in glob.glob(f'{path}/*')]
    if 'scripts' in subfolder_names and 'sprites' in subfolder_names:
        return path
    else:
        if path.parent != path:
            return current_path_or_parent(path.parent)
        else:
            raise FileNotFoundError


def get_sprite_paths(root_path):
    return f"{root_path}/sprites/"
