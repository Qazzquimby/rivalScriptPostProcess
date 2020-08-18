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
        self.code_gml, self.define_gml = self._init_gml()
        self.used_dependencies = self.init_used_dependencies()

    def _init_gml(self) -> t.Tuple[str, str]:
        text = open(self.path).read()

        headers = (script_process.styling.CODE, script_process.styling.DEFINES_AND_MACROS)
        for header in headers:
            pattern = rf"{header[0]}(.*){header[1]}"
            text = re.sub(pattern, '', text)

        splits = text.split('#')
        code_gml = splits[0].strip()
        try:
            define_gml = '#' + splits[1].strip()
        except IndexError:
            define_gml = ''

        return code_gml, define_gml

    def init_used_dependencies(self) -> "script_process.dependencies.ScriptDependencies":
        used = collections.defaultdict(script_process.o_set.OrderedSet)

        for dependency in script_process.library.DEPENDENCIES:
            if uses_dependency(self.code_gml + self.define_gml, dependency):

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
        import_code_gml = generate_init_gml(dependencies)
        import_define_gml = generate_define_gml(dependencies)

        new_gml = '\n\n'.join([self.code_gml, import_code_gml, self.define_gml, import_define_gml])
        open(self.path, 'w').write(new_gml)


def generate_init_gml(dependencies: script_process.o_set.OrderedSet) -> str:
    return generate_gml_for_dependency_type(
        dependencies=dependencies,
        dependency_type=script_process.dependencies.Init,
        headers=script_process.styling.CODE
    )


def generate_define_gml(dependencies: script_process.o_set.OrderedSet) -> str:
    return generate_gml_for_dependency_type(
        dependencies=dependencies,
        dependency_type=script_process.dependencies.Define,
        headers=script_process.styling.DEFINES_AND_MACROS
    )


def generate_gml_for_dependency_type(
        dependencies: script_process.o_set.OrderedSet,
        dependency_type: t.Type[script_process.dependencies.Dependency],
        headers: t.Tuple[str, str]
) -> str:
    dependencies = [dependency for dependency in dependencies if isinstance(dependency, dependency_type)]
    contents = '\n\n'.join([depend.gml for depend in dependencies])
    gml = f"{headers[0]}\n{contents}\n{headers[1]}"
    return gml


def uses_dependency(gml: str, dependency: script_process.dependencies.Dependency) -> bool:
    return re.search(dependency.pattern, gml) is not None
