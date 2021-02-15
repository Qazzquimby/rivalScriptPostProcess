import library.caching
import library.dynamics
from script_process.dependencies import Define

add_to_watches = Define(
    name="add_to_watches",
    version=0,
    params=["_var_name"],
    depends=[library.caching.create_list_if_not_exists],
    docs="""\
    Add the variable name to a list of variables to watch for changes.
    Variables watched will have a `prev__<varname>` stored to track changes.""",
    gml="""\
    //This has too much overhead right now.
    //Replace watches with a set with constant time contains operation?
    create_list_if_not_exists("__WATCHES")
    if ds_list_find_index(__WATCHES, _var_name) == -1 {
        ds_list_add(__WATCHES, _var_name)
    }"""
)

# noinspection PyProtectedMember
update_prev_value = Define(
    name="update_prev_value",
    version=0,
    depends=[library.dynamics.get, library.dynamics._set],
    params=['_name'],
    docs="""\
    Updates a `prev__<varname> variable with the value of the variable last frame.""",
    gml="""\
    var new_value = variable_instance_get(self, name)
    variable_instance_set(self, get_prev_name(name), new_value)"""

)

run_all_update_prev_values = Define(
    name="run_all_update_prev_values",
    version=0,
    depends=[update_prev_value],
    script_path='update.gml', #todo make sure this is actually used
    docs="""\
    Updates the `prev__<varname>` variables for all watched variables on all objects.
    This should be placed with getting targets from a register rather than targeting everything, 
        for better runtime.""",
    gml="""\
    if "__WATCHES" in self {
        for (var watch_i = 0; watch_i < ds_list_size(__WATCHES); watch_i++){
            var watch = __WATCHES[| watch_i];
            update_prev_value(watch);
        }
    }"""
)

value_changed = Define(
    name='value_changed',
    version=0,
    params=['_name'],
    depends=[add_to_watches],
    docs="""\
    Gets if the value with the given name changed since last frame.""",
    gml="""\
    add_to_watches(_name)
    var new_value = get(_name)
    var prev_name = get_prev_name(_name)
    var prev_value = get(prev_name)
    return prev_value != new_value"""
)

DEPENDENCIES = [
    add_to_watches,
    update_prev_value,
    run_all_update_prev_values,
    value_changed
]