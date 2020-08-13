from script_process.dependencies import Define

make_attack = Define(
    name="make_attack",
    version=0,
    docs="""\
    make_attack(_attack_name, (value_name, value)... )
    Sets attack values for the given attack.
    e.g. make_attack(AT_BAIR,
            AG_CATEGORY, 1,
            AG_SPRITE, sprite_get("bair")
        );
    """,
    gml="""\
        var _attack_name = argument[0];
        for(var i = 1; i <= argument_count-1; i+=2) {
            set_attack_value(
                _attack_name, argument[i], argument[i+1]
            )
        }"""
)

make_window = Define(
    name="make_window",
    version=0,
    docs="""\
    make_window(_attack_name, _index, (value_name, value)... )
    Sets window values for the given window.
    e.g.make_window(AT_BAIR, 1,
            AG_WINDOW_TYPE, 1,
            AG_WINDOW_LENGTH, 6
        );
    """,
    gml="""\
        var _attack_name = argument[0];
        var _index = argument[1];
        for(var i = 2; i <= argument_count-1; i+=2) {
            set_window_value(
                _attack_name, _index, argument[i], argument[i+1]
            )
        }"""
)

make_hitbox = Define(
    name="make_hitbox",
    version=0,
    docs="""\
    make_hitbox(_attack_name, _index, (value_name, value)... )
    Sets hitbox values for the given hitbox.
    e.g. make_hitbox(AT_BAIR, 1,
            HG_PARENT_HITBOX, 1,
            HG_HITBOX_TYPE, 1
        );
    """,
    gml="""\
        var _attack_name = argument[0];
        var _index = argument[1];
        for(var i = 2; i <= argument_count-1; i+=2) {
            set_hitbox_value(
                _attack_name, _index, argument[i], argument[i+1]
            )
        }"""
)

DEPENDENCIES = [
    make_attack,
    make_window,
    make_hitbox
]
