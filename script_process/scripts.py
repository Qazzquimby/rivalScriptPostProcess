import collections
import os
import re

import script_process.assets
import script_process.o_set
import script_process.styling
import typing as t
from script_process.log import log

from script_process.o_set import OrderedSet

ScriptDependencies = t.Dict[str, OrderedSet]

if t.TYPE_CHECKING:
    import script_process.dependencies


class Script:
    def __init__(self, path: str):
        self.path = path
        self.code_gml, self.define_gml = self._init_gml()
        self.used_dependencies = self.init_used_dependencies()
        self.given_dependencies = self.init_given_dependencies()
        self.used_assets = self.init_used_assets()
        log.info(f"Script {self.path}")
        log.info(f"Uses {_list_dependencies(self.used_dependencies)}")
        log.info(f"Supplies {_list_dependencies(self.given_dependencies)}\n")

    def _init_gml(self) -> t.Tuple[str, str]:
        text = open(self.path, errors='ignore').read()

        headers = (script_process.styling.CODE, script_process.styling.DEFINES_AND_MACROS)
        for header in headers:
            pattern = rf"{re.escape(header[0])}(.|\n)*{re.escape(header[1])}"
            text = re.sub(pattern, '', text)

        splits = text.split('#', 1)
        code_gml = splits[0].strip()
        try:
            define_gml = '#' + splits[1].strip()
        except IndexError:
            define_gml = ''

        return code_gml, define_gml

    def get_dependency_script(self, dependency: script_process.dependencies.GmlDependency, root_path: str):
        script_path = dependency.script_path
        if script_path is None:
            script_path = self.path

        if not os.path.isabs(script_path):
            script_path = root_path + script_path

        return script_path

    def init_given_dependencies(self) -> ScriptDependencies:
        return self._get_dependencies_that_match_pattern(lambda dependency: dependency.give_pattern)

    def init_used_dependencies(self) -> ScriptDependencies:
        return self._get_dependencies_that_match_pattern(lambda dependency: dependency.use_pattern)

    def init_used_assets(self) -> t.List[script_process.assets.Asset]:
        assets = []
        for asset_type in script_process.assets.ASSET_TYPES:
            assets += asset_type.get_from_text(self.code_gml)
            assets += asset_type.get_from_text(self.define_gml)
        return assets

    def _get_dependencies_that_match_pattern(self, pattern_getter) -> ScriptDependencies:
        dependencies = collections.defaultdict(script_process.o_set.OrderedSet)
        root_path = self.path.split('scripts')[0]

        for dependency in script_process.dependencies.get_dependencies_from_library():
            self._add_dependency_if_used(
                dependencies=dependencies, dependency=dependency, pattern_getter=pattern_getter, root_path=root_path)

        return dependencies

    def _add_dependency_if_used(
            self,
            dependencies: ScriptDependencies,
            dependency,
            pattern_getter,
            root_path
    ):
        try:
            pattern = pattern_getter(dependency)
            if re.search(pattern, self.code_gml + self.define_gml):
                dependencies[self.get_dependency_script(dependency, root_path)].add(dependency)
                for further_depend in dependency.depends:
                    dependencies[self.get_dependency_script(further_depend, root_path)].add(further_depend)
        except AttributeError:
            pass

    def update_dependencies(self, dependencies: script_process.o_set.OrderedSet):
        self._update_dependencies(dependencies)

    def _update_dependencies(self, dependencies: script_process.o_set.OrderedSet):
        dependencies.discard_all(self.given_dependencies[self.path])
        import_code_gml = generate_init_gml(dependencies)
        import_define_gml = generate_define_gml(dependencies)
        new_gml = '\n\n'.join([self.code_gml, import_code_gml, self.define_gml, import_define_gml])
        open(self.path, 'w').write(new_gml)

    def _update_assets(self, assets: t.List[script_process.assets.Asset]):
        for asset in assets:
            print(asset)
        print('debug')  # todo


def _list_dependencies(dependencies):
    return [(path, [depend.name for depend in depends]) for path, depends in dependencies.items()]


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
        dependency_type: t.Type[script_process.dependencies.GmlDependency],
        headers: t.Tuple[str, str]
) -> str:
    dependencies = [dependency for dependency in dependencies if isinstance(dependency, dependency_type)]
    if dependencies:
        contents = '\n\n'.join([depend.gml for depend in dependencies])
        gml = f"{headers[0]}\n{contents}\n{headers[1]}"
        return gml
    else:
        return ''


def uses_dependency(gml: str, dependency: script_process.dependencies.GmlDependency) -> bool:
    return re.search(dependency.use_pattern, gml) is not None
