import abc
import collections
import glob
import os
import pathlib
import re
import typing as t

import script_process.assets
import script_process.sprite_offsets
import script_process.paths
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

        # headers = (CodeDependencyGroup.script_process.styling.CODE, script_process.styling.DEFINES_AND_MACROS)
        dependency_groups = [CodeDependencyGroup(), DeclarationDependencyGroup()]
        for dependency_group in dependency_groups:
            pattern = rf"{re.escape(dependency_group.start_header)}(.|\n)*{re.escape(dependency_group.end_header)}"
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
            if pattern is not None and re.search(pattern, self.code_gml + self.define_gml):
                dependencies[self.get_dependency_script(dependency, root_path)].add(dependency)
                for further_depend in dependency.depends:
                    dependencies[self.get_dependency_script(further_depend, root_path)].add(further_depend)
        except AttributeError:
            pass

    def update_dependencies(self, dependencies: script_process.o_set.OrderedSet):
        dependencies.discard_all(self.given_dependencies[self.path])
        code_gml = CodeDependencyGroup().generate_gml(dependencies)
        declaration_gml = DeclarationDependencyGroup().generate_gml(dependencies)
        parts = [self.code_gml, code_gml, self.define_gml, declaration_gml]
        new_gml = '\n\n'.join(parts)
        open(self.path, 'w').write(new_gml)


class LoadGmlScript(Script):
    def __init__(self, path: str):
        super().__init__(path)
        self.used_dependencies[path].add_all(self.get_missing_offsets())

    def get_missing_offsets(self):
        missing_offset_sprite_paths = self._get_missing_offset_sprite_paths()
        sprite_offset_dependencies = [script_process.sprite_offsets.SpriteOffsetDependency(path)
                                      for path in missing_offset_sprite_paths]
        return sprite_offset_dependencies

    def _get_missing_offset_sprite_paths(self):
        root_path = script_process.paths.get_root_path(self.path)
        sprite_paths = glob.glob(f"{script_process.paths.get_sprite_paths(root_path)}/*.png")
        missing_offset_sprite_paths = [path for path in sprite_paths
                                       if not self._is_already_in_load(path)]
        return missing_offset_sprite_paths

    def _is_already_in_load(self, sprite_path):
        sprite_name = pathlib.Path(sprite_path).stem
        pattern = self._supplies_sprite_offset_pattern(sprite_name)
        return re.match(pattern=pattern, string=self.code_gml)

    def _supplies_sprite_offset_pattern(self, sprite_name):
        return fr'(^|\W)sprite_change_offset\("{sprite_name}",'


def make_script(path: str):
    """Returns the Script class corresponding to the path"""
    if path.endswith('load.gml'):
        cls = LoadGmlScript
    else:
        cls = Script
    return cls(path)


def _list_dependencies(dependencies):
    return [(path, [depend.name for depend in depends]) for path, depends in dependencies.items()]


class DependencyGroup(abc.ABC):
    header_name: str = NotImplemented
    dependency_types: t.List[t.Type] = NotImplemented

    @property
    def start_header(self):
        return f"// vvv {self.header_name} vvv"

    @property
    def end_header(self):
        return f"// ^^^ END: {self.header_name} ^^^"

    def generate_gml(self, dependencies: script_process.o_set.OrderedSet) -> str:
        dependencies = [dependency for dependency in dependencies
                        if isinstance(dependency, tuple(self.dependency_types))]
        if dependencies:
            contents = '\n\n'.join([depend.gml for depend in dependencies])
            gml = f"{self.start_header}\n{contents}\n{self.end_header}"
            return gml
        else:
            return ''


class CodeDependencyGroup(DependencyGroup):
    header_name = "LIBRARY CODE"
    dependency_types = [
        script_process.dependencies.Init,
        script_process.sprite_offsets.SpriteOffsetDependency
    ]


class DeclarationDependencyGroup(DependencyGroup):
    header_name = "LIBRARY DEFINES AND MACROS"
    dependency_types = [
        script_process.dependencies.Define,
        script_process.dependencies.Macro
    ]
