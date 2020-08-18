def _start(name):
    return f"// vvv {name} vvv"


def _end(name):
    return f"// ^^^ END: {name} ^^^"


_code = "LIBRARY CODE"
START_CODE = _start(_code)
END_CODE = _end(_code)
CODE = (START_CODE, END_CODE)

_defines = "LIBRARY DEFINES AND MACROS"
START_DEFINES_AND_MACROS = _start(_defines)
END_DEFINES_AND_MACROS = _end(_defines)
DEFINES_AND_MACROS = (START_DEFINES_AND_MACROS, END_DEFINES_AND_MACROS)
