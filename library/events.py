from script_process.dependencies import Define

run_if_exists = Define(
    name="run_if_exists",
    version=0,
    docs="""\
    (script_name, ...args)
    If the script with the given name exists, call it with the provided arguments.""",
    gml="""\
    script_name = argument[0]
    script_index = script_get_index(script_name)
    if script_index >= 0 {
        var args = array_create(argument_count);
        for (var i = 1; i < argument_count; i++) args[i] = argument[i];
        
        var num_args_to_pass = argument_count - 1;
        switch(num_args_to_pass) {
            case 0: script_execute(script_index); break;
            case 1: script_execute(script_index, args[1]); break;
            case 2: script_execute(script_index, args[1], args[2]); break;
            case 3: script_execute(script_index, args[1], args[2], args[3]); break;
            default: var crash_var = 1/0 break; // Crash. Add more support for the number of arguments you need.
        }
    }""")

# todo update with access to globals if available
