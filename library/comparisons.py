import script_process.dependencies

is_in_range = script_process.dependencies.Define(
    name="is_in_range",
    version=0,
    docs="""\
    Prints each parameter to console, separated by spaces.""",
    params=['_value', '_min', '_max'],
    gml="""\
    return _value == clamp(_value, _min, _max)
    """)


DEPENDENCIES = [
    is_in_range
]
