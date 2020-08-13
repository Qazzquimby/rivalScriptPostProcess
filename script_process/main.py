import script_process.o_set
from script_process.dependencies import Dependency
from script_process.library import DEPENDENCIES
import typing as t
import re
import glob

IMPORT_HEADER = "// *** LIBRARY IMPORTS ***"


def find_missing_dependencies(gml: str) -> script_process.o_set.OrderedSet:
    missing = script_process.o_set.OrderedSet()
    for dependency in DEPENDENCIES:
        if is_missing_dependency(gml, dependency):
            missing.add(dependency)
            for further_depend in dependency.depends:
                missing.add(further_depend)
    return missing


def is_missing_dependency(gml: str, dependency: Dependency) -> bool:
    return re.search(dependency.pattern, gml) is not None


def generate_import_gml(dependencies: script_process.o_set.OrderedSet) -> str:
    dependency_gml = '\n\n'.join([dependency.gml for dependency in dependencies])
    import_gml = f"{IMPORT_HEADER}\n" + dependency_gml
    return import_gml


def get_gml_from_path(path: str) -> str:
    text = open(path).read()
    gml = text.split(IMPORT_HEADER)[0]
    return gml


def process_script(path: str):
    old_gml = get_gml_from_path(path)
    new_gml = get_new_gml(old_gml)
    open(path, 'w').write(new_gml)


def get_new_gml(old_gml: str):
    """Gets dependencies and adds them to the bottom."""
    missing = find_missing_dependencies(old_gml)
    import_gml = generate_import_gml(dependencies=missing)
    return '\n\n'.join([old_gml, import_gml])


def process_all_scripts():
    paths = glob.glob('scripts/*.gml')
    for path in paths:
        process_script(path)


if __name__ == '__main__':
    process_script('scripts/test.gml')
    print('debug')
