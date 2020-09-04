import os
import re
import sys
import abc
import functools
import glob
import inspect
import textwrap
import typing as t
from script_process.log import log
from script_process.o_set import OrderedSet


class Dependency(abc.ABC):
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


ScriptDependencies = t.Dict["Script", OrderedSet]


class Define(Dependency):
    IDENTIFIER_STRING = '#define'

    def __init__(
            self,
            name: str,
            version: int,
            docs: str,
            gml: str,
            depends: t.List[Dependency] = None,
            params: t.List[str] = None,
            script_path: str = None
    ):
        super().__init__(
            name=name,
            depends=depends,
            gml=self._init_gml(name, params, version, docs, gml),
            use_pattern=fr'(^|\W){name}\(',
            give_pattern=fr'{self.IDENTIFIER_STRING}(\s)*{name}(\W|$)',
            script_path=script_path
        )

    @staticmethod
    def _init_gml(name, params, version, docs, gml):
        if params is None:
            params = []
        if len(params) > 0:
            param_string = f"({', '.join(params)})"
        else:
            param_string = ''

        head = f"{Define.IDENTIFIER_STRING} {name}{param_string}"
        docs = textwrap.indent(textwrap.dedent(docs), '    // ')
        gml = textwrap.indent(textwrap.dedent(gml), '    ')
        final = f"{head} // Version {version}\n{docs}\n{gml}"
        return textwrap.dedent(final).strip()

    @staticmethod
    def from_gml(in_gml: str):
        name_params_version, content = in_gml.split('\n', 1)
        name, params, version = Define._extract_name_params_version(name_params_version)

        docs, gml = Define._extract_docs_gml(content)

        return Define(
            name=name,
            params=params,
            version=version,
            docs=docs,
            gml=gml)

    @staticmethod
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

    @staticmethod
    def _extract_docs_gml(docs_gml: str) -> t.Tuple[str, str]:
        content_lines = docs_gml.split('\n')
        doc_lines = []
        gml_lines = []
        is_docs = True
        for line in content_lines:
            if is_docs:
                if line.replace(' ', '').replace('\t', '').startswith('//'):
                    line = re.sub(r'//\s*', '', line)
                    doc_lines.append(line)
                else:
                    is_docs = False
            if not is_docs:
                gml_lines.append(line)

        docs = '\n'.join(doc_lines)
        gml = '\n'.join(gml_lines)
        return docs, gml


class Init(Dependency):
    def __init__(
            self,
            name: str,
            gml: str,
            docs: str = "",
            depends: t.List[Dependency] = None,
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


@functools.lru_cache()
def get_dependencies_from_library():
    project_path = os.getcwd()  # os.path.dirname(os.path.dirname(__file__))
    log.info(f"Project path: {project_path}")
    sys.path.append(project_path)
    log.info(f"Sys path: {sys.path}")
    plugin_root = "library"
    plugin_paths = glob.glob(f"{plugin_root}/*.py")
    log.info(f"Plugin paths: {plugin_paths}")

    library_members = set()
    for path in plugin_paths:
        plugin_import = path.replace('.py', '').replace('\\', '.')
        plugin_modules = inspect.getmembers(__import__(plugin_import), inspect.ismodule)
        for _, plugin_module in plugin_modules:
            for member in vars(plugin_module).values():
                if isinstance(member, Dependency):
                    library_members.add(member)

    custom_imports = get_imports_gml()
    log.info(f"Custom imports: {[member.name for member in custom_imports]}\n")

    library_members.update(custom_imports)
    log.info(f"Library contents: {[member.name for member in library_members]}\n")
    return library_members


def get_imports_gml():
    custom_imports_text = open('scripts/imports.gml').read()

    import_texts = ['#' + import_text for import_text in custom_imports_text.split('#') if len(import_text) > 0]
    dependencies = [make_dependency(import_text) for import_text in import_texts]

    return set(dependencies)


def make_dependency(in_gml: str) -> Dependency:
    if in_gml.startswith(Define.IDENTIFIER_STRING):
        return Define.from_gml(in_gml)
    raise ValueError("Given gml doesn't look like a support dependency.")
