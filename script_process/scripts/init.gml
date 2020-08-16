print(blah)

// *** LIBRARY IMPORTS ***
// Lists attack IDs.
lib_attacks = [
    AT_JAB,
    AT_DATTACK,
    AT_FTILT,
    AT_DTILT,
    AT_UTILT,
    AT_FSTRONG,
    AT_DSTRONG,
    AT_USTRONG,
    AT_FAIR,
    AT_BAIR,
    AT_DAIR,
    AT_UAIR,
    AT_NAIR,
    AT_FSPECIAL,
    AT_DSPECIAL,
    AT_USPECIAL,
    AT_NSPECIAL,
    AT_TAUNT
]
#define print //Version 0
    // Prints each parameter to console, separated by spaces.
    var _out_string = ""
    for (var i = 0; i < argument_count; i++){
        _out_string += string(argument[i])
        _out_string += " "
    }
    print_debug(_out_string)