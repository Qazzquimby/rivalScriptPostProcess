import os
import re
import sys
import abc
import functools
import glob
import inspect
import textwrap
import typing as t

import script_process.pattern_matching
from script_process.log import log
from script_process.o_set import OrderedSet


class GmlDependency(abc.ABC):
    def __init__(self,
                 name: str,
                 depends: t.Optional[OrderedSet],
                 gml: str,
                 use_pattern: str,
                 give_pattern: str,
                 script_path: str = None):
        self.name = name
        if depends is None:
            depends = OrderedSet()
        self.depends = OrderedSet(depends)
        self.gml = gml
        self.use_pattern = use_pattern
        self.give_pattern = give_pattern
        self.script_path = script_path

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def _init_gml(
        type_id: str, name: str, params: t.List[str], version: int, docs: str, gml: str
):
    """Serialize the gml elements into the final gml structure."""
    if params is None:
        params = []
    if len(params) > 0:
        param_string = f"({', '.join(params)})"
    else:
        param_string = ''

    head = f"{type_id} {name}{param_string}"
    docs = textwrap.indent(textwrap.dedent(docs), '    // ')
    gml = textwrap.indent(textwrap.dedent(gml), '    ')
    final = f"{head} // Version {version}\n{docs}\n{gml}"
    return textwrap.dedent(final).strip()


ScriptDependencies = t.Dict["Script", OrderedSet]


class Define(GmlDependency):
    IDENTIFIER_STRING = '#define'

    def __init__(
            self,
            name: str,
            version: int,
            docs: str,
            gml: str,
            depends: t.List[GmlDependency] = None,
            params: t.List[str] = None,
            script_path: str = None
    ):
        super().__init__(
            name=name,
            depends=depends,
            gml=_init_gml(self.IDENTIFIER_STRING, name, params, version, docs, gml),
            use_pattern=script_process.pattern_matching.uses_function_pattern(name),
            give_pattern=fr'{self.IDENTIFIER_STRING}(\s)*{name}(\W|$)',
            script_path=script_path
        )


class Macro(GmlDependency):
    IDENTIFIER_STRING = '#macro'

    def __init__(
            self,
            name: str,
            version: int,
            docs: str,
            gml: str,
            depends: t.List[GmlDependency] = None,
            params: t.List[str] = None,
            script_path: str = None
    ):
        super().__init__(
            name=name,
            depends=depends,
            gml=_init_gml(self.IDENTIFIER_STRING, name, params, version, docs, gml),
            use_pattern=fr'(^|\W){name}',
            give_pattern=fr'{self.IDENTIFIER_STRING}(\s)*{name}(\W|$)',
            script_path=script_path
        )


def make_dependency(in_gml: str, dependencies=None):
    """Deserializes the gml into the correct Dependency subclass"""
    if dependencies is None:
        dependencies = []

    name_params_version, content = in_gml.split('\n', 1)
    name, params, version = _extract_name_params_version(name_params_version)

    docs, gml = _extract_docs_gml(content)
    used_dependencies = [dependency for dependency in dependencies if re.search(dependency.use_pattern, gml)]

    for dependency_type in (Define, Macro):
        if in_gml.startswith(dependency_type.IDENTIFIER_STRING):
            return dependency_type(
                name=name,
                params=params,
                version=version,
                docs=docs,
                gml=gml,
                depends=used_dependencies)
    raise ValueError("Given gml doesn't look like a support dependency.")


def _extract_name_params_version(name_params_version_line: str) -> t.Tuple[str, t.List[str], int]:
    name_params_version = name_params_version_line.replace(Define.IDENTIFIER_STRING, '').strip()
    has_version = '//' in name_params_version
    if has_version:
        name_params, version_str = [section.strip() for section in name_params_version.split('//')]
        version = int(re.findall(r'\d+', version_str)[0])
    else:
        name_params = name_params_version
        version = 0

    has_params = '(' in name_params
    if has_params:
        name, params_str = name_params.split('(')
        params = params_str.replace(')', '').replace(' ', '').split(',')
    else:
        name = name_params
        params = []
    return name, params, version


def _is_documentation_line(line: str) -> bool:
    return line.replace(' ', '').replace('\t', '').startswith('//')


def _remove_documentation_prefix_from_line(line: str) -> str:
    return re.sub(r'//\s*', '', line)


def _extract_docs_gml(docs_gml: str) -> t.Tuple[str, str]:
    content_lines = docs_gml.split('\n')
    doc_lines = []
    gml_lines = []
    for line in content_lines:
        if not gml_lines and _is_documentation_line(line):
            line = _remove_documentation_prefix_from_line(line)
            doc_lines.append(line)
        else:
            gml_lines.append(line)

    docs = '\n'.join(doc_lines)
    gml = '\n'.join(gml_lines)
    return docs, gml


class Init(GmlDependency):
    def __init__(
            self,
            name: str,
            gml: str,
            docs: str = "",
            depends: t.List[GmlDependency] = None,
            script_path: str = 'scripts\\init.gml'
    ):
        super().__init__(
            name=name,
            depends=depends,
            gml=self._init_gml(name, docs, gml),
            use_pattern=fr'(^|\W){name}(\W|$)',
            give_pattern=fr'(^|\W){name}(\s)*=',
            script_path=script_path
        )

    @staticmethod
    def _init_gml(name, docs, gml):
        docs = textwrap.indent(textwrap.dedent(docs), '// ').strip()
        gml = textwrap.dedent(gml)
        final = f"{docs}\n{name} = {gml}"
        return textwrap.dedent(final).strip()


def _get_plugin_paths():
    project_path = os.getcwd()  # os.path.dirname(os.path.dirname(__file__))
    sys.path.append(project_path)
    plugin_root = "library"
    plugin_paths = glob.glob(f"{plugin_root}/*.py")

    log.info(f"Project path: {project_path}")
    log.info(f"Sys path: {sys.path}")
    log.info(f"Plugin paths: {plugin_paths}")
    return plugin_paths


def get_dependencies_from_path(path: str) -> t.Set[GmlDependency]:
    dependencies_at_path = set()
    plugin_import = path.replace('.py', '').replace('\\', '.')
    plugin_modules = inspect.getmembers(__import__(plugin_import), inspect.ismodule)
    for _, plugin_module in plugin_modules:
        for member in vars(plugin_module).values():
            if isinstance(member, GmlDependency):
                dependencies_at_path.add(member)
    return dependencies_at_path


@functools.lru_cache()
def get_dependencies_from_library() -> t.Set[GmlDependency]:
    plugin_paths = _get_plugin_paths()

    library_members = set()
    for path in plugin_paths:
        dependencies_at_path = get_dependencies_from_path(path)
        library_members.update(dependencies_at_path)

    add_custom_dependencies(library_members)
    log.info(f"Library contents: {[member.name for member in library_members]}\n")
    return library_members


def add_custom_dependencies(lib_dependencies):
    try:
        custom_imports_text = open('scripts/imports.gml').read()
    except FileNotFoundError:
        return

    import_texts = ['#' + import_text.strip()
                    for import_text in custom_imports_text.split('#')
                    if len(import_text.strip()) > 0]

    for import_text in import_texts:
        new_dependency = make_dependency(import_text, lib_dependencies)
        lib_dependencies.add(new_dependency)
