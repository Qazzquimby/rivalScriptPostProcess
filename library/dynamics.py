from script_process.dependencies import Define

run_if_exists_with_args = Define(
    name="run_if_exists_with_args",
    version=0,
    docs="""\
    If the script with the given name exists, call it with the unpacked list of arguments.
    Currently supports up to 7 arguments. Modify the switch statement if you need more.
    """,
    gml="""\
    #define run_if_exists_with_args(script_name, args)
    var script_index = script_get_index(script_name)
    if script_index >= 0 {       
        var num_args_to_pass = array_length(args);
        switch(num_args_to_pass) {
            case 0: script_execute(script_index); break;
            case 1: script_execute(script_index, args[0]); break;
            case 2: script_execute(script_index, args[0], args[1]); break;
            case 3: script_execute(script_index, args[0], args[1], args[2]); break;
            case 4: script_execute(script_index, args[0], args[1], args[2], args[3]); break;
            case 5: script_execute(script_index, args[0], args[1], args[2], args[3], args[4]); break;
            case 6: script_execute(script_index, args[0], args[1], args[2], args[3], args[4], args[5]); break;
            case 7: script_execute(script_index, args[0], args[1], args[2], args[3], args[4], args[5], args[6]); break;
            default: var crash_var = 1/0 break; // Crash. Add more support for the number of arguments you need.
        }
    }"""
)

run_if_exists = Define(
    name="run_if_exists",
    version=0,
    depends=[run_if_exists_with_args],
    docs="""\
    (script_name, ...args)
    If the script with the given name exists, call it with the provided arguments.""",
    gml="""\
    var script_name = argument[0]
    var num_args = argument_count - 1;
    var args = array_create(num_args);
    for (var i = 0; i < num_args; i++) args[i] = argument[i+1];
    run_if_exists_with_args(script_name, args)
    """)

get_defines = Define(
    name="get_defines",
    version=0,
    docs="""\
    Create a new list containing the names of all defines in the current script.""",
    gml="""\
    var defines = ds_list_create()
    
    var i = 2
    while(true) {
        var name = script_get_name(i)
        if name == undefined {
            break;
        } else {
            ds_list_add(defines, name)
            i += 1
        }
    }
    return defines;"""
)

get_systems = Define(
    name="get_systems",
    version=0,
    depends=[get_defines],
    docs="""\
    Returns all defines in this script that start with `run_`, in order from top to bottom.""",
    gml="""\
    if "__SYSTEMS" in self {
        return __SYSTEMS
    } else {
        __SYSTEMS = ds_list_create()
        var defines = get_defines();
        for (var i = 0; i < ds_list_size(defines); i++){
            var define = defines[|i];
            if string_pos('run_', define) == 1 {
                ds_list_add(__SYSTEMS, define);
            }
        }
        return systems;
    }
    """,
)

run_for_players = Define(
    name="run_for_players",
    version=0,
    params=['script_name'],
    depends=[run_if_exists],
    docs="""\
    Run the named script for each oPlayer.
    This may later be expanded to run on player-like articles.""",
    gml="""\
    with asset_get("oPlayer") {
        run_if_exists(script_name)
    }"""
)

run_for_articles = Define(
    name="run_for_articles",
    version=0,
    params=['script_name'],
    depends=[run_if_exists],
    docs="""\
    Run the named script for each of instance of each kind of article.""",
    gml="""\
    with asset_get("obj_article1") {
        run_if_exists(script_name)
    }
    with asset_get("obj_article2") {
        run_if_exists(script_name)
    }
    with asset_get("obj_article3") {
        run_if_exists(script_name)
    }
    with asset_get("obj_article_solid") {
        run_if_exists(script_name)
    }
    with asset_get("obj_article_platform") {
        run_if_exists(script_name)
    }"""
)

run_for_all = Define(
    name="run_for_all",
    version=0,
    params=['script_name'],
    depends=[run_for_players, run_for_articles],
    docs="""\
    Run the named script for each of instance of oPlayer and each kind of article.""",
    gml="""\
    run_for_players(script_name)
    run_for_articles(script_name)"""
)

run_systems = Define(
    name="run_systems",
    version=0,
    depends=[get_systems, run_for_all, run_for_players, run_for_articles, run_if_exists],
    docs="""\
    Run each define in this script that starts with `run_` in order from top to bottom.
    With format `run_all_...` will run on all objects. 
    With format `run_player_...` will run on oPlayer instances.
    With format `run_instance_...` will run on all article instances.""",
    gml="""\
    var systems = get_systems()
    for (var system_i = 0; system_i < ds_list_size(systems); system_i++){
        var system = systems[| system_i];
        if string_pos('all_', system) == 5 {
            run_for_all(system);
        } else if string_pos('player_', system) == 5 {
            run_for_players(system);
        } else if string_pos('article_', system) == 5 {
            run_for_articles(system);
        } 
        else {
            run_if_exists(system)
        }
    }"""
)

get = Define(
    name="get",
    version=0,
    params=['_name'],
    docs="""\
    Gets the variable with the given name from self.""",
    gml="""\
    return variable_instance_get(self, _name)"""
)

_set = Define(
    name="set",
    version=0,
    params=['_name', '_value'],
    docs="""\
    Sets the variable with the given name from self to the given value.""",
    gml="""\
    variable_instance_set(self, _name, _value)"""
)

DEPENDENCIES = [
    run_if_exists,
    run_if_exists_with_args,
    get_defines,
    get_systems,
    run_for_all,
    run_for_players,
    run_for_articles,
    run_systems,
    get,
    _set,
]
