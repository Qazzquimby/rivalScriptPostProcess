import collections
import os

import script_process.dependencies
import script_process.o_set
import typing as t
from script_process.scripts import Script
import glob
from script_process.log import log


class CharacterScriptProcessor:
    def __init__(self):
        self.paths_to_scripts, self.custom_imports = get_paths_to_scripts_and_custom_imports()
        self.dependencies = merge_dependencies([script.used_dependencies for script in self.paths_to_scripts.values()])
        self.update()

    def update(self):
        """Gets dependencies and adds them to the bottom."""
        for path, dependencies in self.dependencies.items():
            try:
                self.paths_to_scripts[path].update(dependencies)
            except KeyError:
                open(path, 'w+')  # makes empty file
                script = Script(path)
                script.update(dependencies)


def get_paths_to_scripts_and_custom_imports() -> t.Tuple[t.Dict[str, Script], t.Optional[Script]]:
    log.debug(f"cwd: {os.getcwd()}")
    paths = glob.glob('scripts/**/*.gml', recursive=True)
    log.debug(f"paths: {paths}\n")
    paths_to_scripts = {path: Script(path) for path in paths}

    custom_imports = None
    for path in paths_to_scripts.keys():
        if path.endswith('imports.gml'):
            custom_imports = paths_to_scripts.pop(path)
        break

    return paths_to_scripts, custom_imports


def merge_dependencies(dependency_trees: t.List[t.Dict[str, script_process.dependencies.Dependency]]):
    merged = collections.defaultdict(script_process.o_set.OrderedSet)
    for dependency_tree in dependency_trees:
        for path, dependencies in dependency_tree.items():
            merged[path].add_all(dependencies)
    return merged


if __name__ == '__main__':
    log.info("Starting")
    CharacterScriptProcessor()
    log.info("Finished")
