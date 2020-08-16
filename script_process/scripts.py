import collections
import re

import script_process.library
import script_process.o_set
import script_process.styling
import typing as t

if t.TYPE_CHECKING:
    import script_process.dependencies


class Script:
    def __init__(self, path: str):
        self.path = path
        self.gml = self._init_gml()
        self.used_dependencies = self.init_used_dependencies()

    def _init_gml(self) -> str:
        text = open(self.path).read()
        gml = text.split(script_process.styling.IMPORT_HEADER)[0].strip()
        return gml

    def init_used_dependencies(self) -> "script_process.dependencies.ScriptDependencies":
        used = collections.defaultdict(script_process.o_set.OrderedSet)

        for dependency in script_process.library.DEPENDENCIES:
            if uses_dependency(self.gml, dependency):

                used[self.get_dependency_script(dependency)].add(dependency)
                for further_depend in dependency.depends:
                    used[self.get_dependency_script(further_depend)].add(further_depend)
        return used

    def get_dependency_script(self, dependency: script_process.dependencies.Dependency):
        script_path = dependency.script_path
        if script_path is None:
            script_path = self.path
        return script_path

    def update(self, dependencies: script_process.o_set.OrderedSet):
        import_gml = generate_import_gml(dependencies=dependencies)
        new_gml = '\n\n'.join([self.gml, import_gml])
        open(self.path, 'w').write(new_gml)


def generate_import_gml(dependencies: script_process.o_set.OrderedSet) -> str:
    init_gml = generate_gml_for_dependency_type(dependencies, script_process.dependencies.Init)
    define_gml = generate_gml_for_dependency_type(dependencies, script_process.dependencies.Define)
    import_gml = f"{script_process.styling.IMPORT_HEADER}\n" + init_gml + "\n" + define_gml
    return import_gml


def generate_gml_for_dependency_type(
        dependencies: script_process.o_set.OrderedSet,
        dependency_type: t.Type[script_process.dependencies.Dependency]
) -> str:
    dependencies = [dependency for dependency in dependencies if isinstance(dependency, dependency_type)]
    gml = '\n\n'.join([depend.gml for depend in dependencies])
    return gml


def uses_dependency(gml: str, dependency: script_process.dependencies.Dependency) -> bool:
    return re.search(dependency.pattern, gml) is not None
