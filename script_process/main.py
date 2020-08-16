import collections

import script_process.dependencies
import script_process.o_set
import typing as t
from script_process.scripts import Script
import glob

class CharacterScriptProcessor:
    def __init__(self):
        self.scripts = get_all_scripts()
        self.dependencies = merge_dependencies([script.used_dependencies for script in self.scripts])
        self.update()

    def update(self):
        """Gets dependencies and adds them to the bottom."""
        for script in self.scripts:
            script.update(self.dependencies[script.path])


def get_all_scripts() -> t.List[Script]:
    paths = glob.glob('scripts/*.gml')
    scripts = [Script(path) for path in paths]
    return scripts


def merge_dependencies(dependency_trees: t.List[t.Dict[str, script_process.dependencies.Dependency]]):
    merged = collections.defaultdict(script_process.o_set.OrderedSet)
    for dependency_tree in dependency_trees:
        for path, dependencies in dependency_tree.items():
            merged[path].add_all(dependencies)
    return merged



if __name__ == '__main__':
    CharacterScriptProcessor()
    print('debug')
