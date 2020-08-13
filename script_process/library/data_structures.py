from script_process.dependencies import Define

Map = Define(
    name="Map",
    version=0,
    docs="""\
    Creates a mapping from each pair of arguments.
    my_map = Map(
        "a", 1,
        "b", 2,
    )
    my_map[?"a"]
    >>> 1
    """,
    gml="""\
    if (argument_count mod 2 != 0) {
        print_debug(`Expected an even number of arguments, got ${string(argument_count)}.`);
    }
    var _map = ds_map_create();
    for (var i = 0; i < argument_count; i += 2) {
        _map[? argument[i]] = argument[i+1];
    }
    return _map;
    """)

DEPENDENCIES = [
    Map
]
