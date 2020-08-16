import abc
import textwrap
import typing as t

from script_process.o_set import OrderedSet

if t.TYPE_CHECKING:
    from script_process.scripts import Script


class Dependency(abc.ABC):
    def __init__(self, name: str, depends: t.Optional[OrderedSet], gml: str, pattern: str, script_path: str = None):
        self.name = name
        if depends is None:
            depends = OrderedSet()
        self.depends = OrderedSet(depends)
        self.gml = gml
        self.pattern = pattern
        self.script_path = script_path

    def __str__(self):
        return self.name


ScriptDependencies = t.Dict["Script", OrderedSet]


class Define(Dependency):
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
            pattern=fr'(^|\W){name}\(',
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

        head = f"#define {name}{param_string}"
        docs = textwrap.indent(textwrap.dedent(docs), '    // ')
        gml = textwrap.indent(textwrap.dedent(gml), '    ')
        final = f"{head} //Version {version}\n{docs}\n{gml}"
        return textwrap.dedent(final).strip()


class Init(Dependency):
    def __init__(
            self,
            name: str,
            docs: str,
            gml: str,
            depends: t.List[Dependency] = None,
            script_path: str = 'scripts/init.gml'
    ):
        super().__init__(
            name=name,
            depends=depends,
            gml=self._init_gml(name, docs, gml),
            pattern=fr'(^|\W){name}(\W|$)',
            script_path=script_path
        )

    @staticmethod
    def _init_gml(name, docs, gml):
        docs = textwrap.indent(textwrap.dedent(docs), '// ')
        final = f"{docs}\n{name} = {gml}"
        return textwrap.dedent(final).strip()
