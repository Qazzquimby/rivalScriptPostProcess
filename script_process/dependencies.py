import abc
import textwrap
import typing as t

import script_process.o_set


class Dependency(abc.ABC):
    def __init__(self, name: str, depends: t.Set["Dependency"], gml: str, pattern: str):
        self.name = name
        self.depends = script_process.o_set.OrderedSet(depends)
        self.gml = gml
        self.pattern = pattern

    def __str__(self):
        return self.name


class Define(Dependency):
    def __init__(
            self,
            name: str,
            version: int,
            docs: str,
            gml: str,
            depends: t.List[Dependency] = None,
            params: t.List[str] = None
    ):
        if depends is None:
            depends = set()
        super().__init__(
            name=name,
            depends=depends,
            gml=self._init_gml(name, params, version, docs, gml),
            pattern=fr'(^|\s){name}\('
        )

    def _init_gml(self, name, params, version, docs, gml):
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
