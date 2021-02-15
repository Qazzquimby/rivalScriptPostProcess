import abc
import textwrap

import parse
from inflector import English

CODE_GEN_MARKER = '$'


class CodeGenerator(abc.ABC):
    parser: parse.Parser = NotImplemented

    def generate_out(self, match):
        raise NotImplementedError


class ForEach(CodeGenerator):
    parser = parse.compile("foreach-{items:l}")

    def generate_out(self, text: str):
        match = self.parser.search(text)
        if not match:
            return None

        items_name = match['items']
        item_name = singularize(items_name)
        iterator_name = f"{item_name}_i"
        return textwrap.dedent(f"""\
        for (var {iterator_name} = 0; {iterator_name}++; {iterator_name} < array_length({items_name}) {{
            var {item_name} = {items_name}[{iterator_name}]
        
        }}""")


CODE_GENERATORS = [
    ForEach()
]


def generate_code_for_line(line: str) -> str:
    before, content, after = line.split(CODE_GEN_MARKER)
    for code_generator in CODE_GENERATORS:
        code = code_generator.generate_out(content)
        if content:
            if before.isspace():
                indented_code = textwrap.indent(text=code, prefix=before)
                return f'{indented_code}{after}'
            else:
                return f'{before}{code}{after}'

    return (f'{before}{CODE_GEN_MARKER}{content}{CODE_GEN_MARKER}{after} '
            f'// ERROR: No code injection match found')


def generate_code(text: str) -> str:
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.count(CODE_GEN_MARKER) == 2:
            lines[i] = generate_code_for_line(line)
    return '\n'.join(lines)


_inflector_singularize = English().singularize


def singularize(string: str):
    string = string.lower()
    inflector_attempt = _inflector_singularize(string)
    if inflector_attempt == string:
        return f"{string}_item"
    else:
        return inflector_attempt


if __name__ == '__main__':
    text = """\
hurtbox_spr = asset_get("ex_guy_hurt_box");
        $foreach-structs$
        
    pratfall_anim_speed = .25; //The speed of your pratfall animation in anim frames per gameplay frame
"""
    result = generate_code(text)
    print(result)
    print('debug')
