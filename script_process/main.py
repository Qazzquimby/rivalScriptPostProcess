import collections
import sys
import typing as t
import glob

import script_process.dependencies
import script_process.assets
import script_process.o_set
from script_process.scripts import Script
from script_process.log import log


class CharacterScriptProcessor:
    def __init__(self, path):
        self.path = path
        self.paths_to_scripts = get_paths_to_scripts(path)
        self.update_dependencies()
        self.update_assets()

    def update_dependencies(self):
        """Gets needed dependencies in the path and supplies them."""
        dependencies = merge_dependencies([script.used_dependencies for script in self.paths_to_scripts.values()])
        for path, dependencies in dependencies.items():
            try:
                self.paths_to_scripts[path].update_dependencies(dependencies)
            except KeyError:
                open(path, 'w+')  # makes empty file
                script = Script(path)
                script.update_dependencies(dependencies)

    def update_assets(self):
        """Gets needed assets in the path and supplies them."""
        assets = merge_assets([script.used_assets for script in self.paths_to_scripts.values()])
        for asset in assets:
            asset.supply(self.path)


def get_paths_to_scripts(root_path: str) -> t.Dict[str, Script]:
    paths = glob.glob(f'{root_path}/scripts/**/*.gml', recursive=True)
    for path in paths:
        if path.endswith('imports.gml'):
            paths.remove(path)
        break
    log.debug(f"paths: {paths}\n")

    paths_to_scripts = {path: Script(path) for path in paths}
    return paths_to_scripts


def merge_dependencies(dependency_trees: t.List[t.Dict[str, script_process.dependencies.GmlDependency]]):
    merged = collections.defaultdict(script_process.o_set.OrderedSet)
    for dependency_tree in dependency_trees:
        for path, dependencies in dependency_tree.items():
            merged[path].add_all(dependencies)
    return merged


def merge_assets(assets_for_scripts: t.List[t.List[script_process.assets.Asset]]) -> t.Set[script_process.assets.Asset]:
    merged_for_scripts = (set(assets_for_script) for assets_for_script in assets_for_scripts)
    merged = set.union(*merged_for_scripts)
    return merged


if __name__ == '__main__':
    log.info("Starting")
    try:
        path_to_process = sys.argv[1]
        CharacterScriptProcessor(path_to_process)
    except Exception as e:
        log.error("Failed with following exception")
        log.error(e, exc_info=True)
        raise e
    log.info("Finished")
