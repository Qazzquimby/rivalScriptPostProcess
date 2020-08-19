import collections
import script_process.dependencies
import script_process.o_set
import typing as t
from script_process.scripts import Script
import glob


class CharacterScriptProcessor:
    def __init__(self):
        self.paths_to_scripts = get_paths_to_scripts()
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


def get_paths_to_scripts() -> t.Dict[str, Script]:
    paths = glob.glob('scripts/*.gml')
    log.debug(f"paths: {paths}")
    paths_to_scripts = {path: Script(path) for path in paths}
    return paths_to_scripts


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
