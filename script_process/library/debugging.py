from script_process.dependencies import Define

print_ = Define(
    name="print",
    version=0,
    docs="""\
    Prints each parameter to console, separated by spaces.""",
    gml="""\
    var _out_string = ""
    for (var i = 0; i < argument_count; i++){
        _out_string += string(argument[i])
        _out_string += " "
    }
    print_debug(_out_string)""")

DEPENDENCIES = [
    print_
]