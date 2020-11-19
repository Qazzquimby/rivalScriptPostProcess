import script_process.dependencies

is_in_range = script_process.dependencies.Define(
    name="is_in_range",
    version=0,
    docs="""\
    Returns whether the value falls within the min and max, inclusive.""",
    params=['_value', '_min', '_max'],
    gml="""\
    return _value == clamp(_value, _min, _max)
    """)


DEPENDENCIES = [
    is_in_range
]
