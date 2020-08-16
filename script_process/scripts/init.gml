print(blah)

// *** LIBRARY IMPORTS ***
#define print //Version 0
    // Prints each parameter to console, separated by spaces.
    var _out_string = ""
    for (var i = 0; i < argument_count; i++){
        _out_string += string(argument[i])
        _out_string += " "
    }
    print_debug(_out_string)