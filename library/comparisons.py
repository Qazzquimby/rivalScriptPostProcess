import script_process.dependencies

is_in_range = script_process.dependencies.Define(
    name="is_in_range",
    version=0,
    params=['_value', '_min', '_max'],
    docs="""\
    Returns whether the value falls within the min and max, inclusive.""",
    gml="""\
    return _value == clamp(_value, _min, _max)
    """)


DEPENDENCIES = [
    is_in_range
]
