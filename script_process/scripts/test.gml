var blah = 1.0
print(blah)
var other = Map(1, 2, 3, 4)
set_state(fff)
set_window(fff)
make_attack()
make_window()
make_hitbox()

lib_attacks

// *** LIBRARY IMPORTS ***

#define print //Version 0
    // Prints each parameter to console, separated by spaces.
    var _out_string = ""
    for (var i = 0; i < argument_count; i++){
        _out_string += string(argument[i])
        _out_string += " "
    }
    print_debug(_out_string)

#define Map //Version 0
    // Creates a mapping from each pair of arguments.
    // my_map = Map(
    //     "a", 1,
    //     "b", 2,
    // )
    // my_map[?"a"]
    // >>> 1

    if (argument_count mod 2 != 0) {
        print_debug(`Expected an even number of arguments, got ${string(argument_count)}.`);
    }
    var _map = ds_map_create();
    for (var i = 0; i < argument_count; i += 2) {
        _map[? argument[i]] = argument[i+1];
    }
    return _map;

#define set_state(_new_state) //Version 0
    // Sets the state to the given state and resets the state timer.
    state = _new_state;
    state_timer = 0;

#define set_window(_new_window) //Version 0
    // Sets the window to the given state and resets the window timer.
    window = _new_window
    window_timer = 0

#define make_attack //Version 0
    // make_attack(_attack_name, (value_name, value)... )
    // Sets attack values for the given attack.
    // e.g. make_attack(AT_BAIR,
    //         AG_CATEGORY, 1,
    //         AG_SPRITE, sprite_get("bair")
    //     );

    var _attack_name = argument[0];
    for(var i = 1; i <= argument_count-1; i+=2) {
        set_attack_value(
            _attack_name, argument[i], argument[i+1]
        )
    }

#define make_window //Version 0
    // make_window(_attack_name, _index, (value_name, value)... )
    // Sets window values for the given window.
    // e.g.make_window(AT_BAIR, 1,
    //         AG_WINDOW_TYPE, 1,
    //         AG_WINDOW_LENGTH, 6
    //     );

    var _attack_name = argument[0];
    var _index = argument[1];
    for(var i = 2; i <= argument_count-1; i+=2) {
        set_window_value(
            _attack_name, _index, argument[i], argument[i+1]
        )
    }

#define make_hitbox //Version 0
    // make_hitbox(_attack_name, _index, (value_name, value)... )
    // Sets hitbox values for the given hitbox.
    // e.g. make_hitbox(AT_BAIR, 1,
    //         HG_PARENT_HITBOX, 1,
    //         HG_HITBOX_TYPE, 1
    //     );

    var _attack_name = argument[0];
    var _index = argument[1];
    for(var i = 2; i <= argument_count-1; i+=2) {
        set_hitbox_value(
            _attack_name, _index, argument[i], argument[i+1]
        )
    }