from . import data_structures
from script_process.dependencies import Init, Define

lib_state_to_sprite_string = Init(
    name="lib_state_to_sprite_string",
    gml="""\
    Map(
        PS_IDLE, "idle",
        PS_WALK, "walk",
        PS_WALK_TURN, "walkturn",
        PS_DASH_TURN, "walkturn",
        PS_DASH_START, "dashstart",
        PS_DASH_STOP, "dashstop",
        PS_DASH, "dash",
        PS_IDLE_AIR, "jump",
        PS_CROUCH,  "crouch",
        PS_JUMPSQUAT, "jumpstart",
        PS_FIRST_JUMP, "jump",
        PS_DOUBLE_JUMP, "doublejump",
        PS_WALL_JUMP, "doublejump",
        PS_LAND, "land",
        PS_WAVELAND, "waveland",
        PS_AIR_DODGE, "airdodge",
        PS_ROLL_BACKWARD, "airdodge",
        PS_ROLL_FORWARD, "airdodge",
        PS_TECH_BACKWARD, "airdodge",
        PS_TECH_FORWARD, "airdodge",
        PS_PARRY, "parry",
        PS_PARRY_START, "parry",
        PS_TECH_GROUND, "tech",
        PS_WALL_TECH, "tech",
        PS_LANDING_LAG, "landinglag",
        PS_PRATLAND, "landinglag",
        PS_HITSTUN, "hurt",
        PS_WRAPPED, "hurt",
        PS_FROZEN, "hurt",
        PS_PRATFALL, "pratfall",
        PS_TUMBLE, "pratfall",
        PS_HITSTUN_LAND, "pratfall",
        PS_SPAWN, "intro",
        PS_RESPAWN, "respawn"
    );""",
    depends=[data_structures.Map]
)

lib_attack_to_sprite_string = Init(
    name="lib_attack_to_sprite_string",
    gml="""\
    Map(
        AT_JAB, "jab",
        AT_FTILT, "ftilt",
        AT_UTILT, "utilt",
        AT_DTILT, "dtilt",
        AT_FSTRONG, "fstrong",
        AT_USTRONG, "ustrong",
        AT_DSTRONG, "dstrong",
        AT_DSPECIAL, "dspecial",
        AT_TAUNT, "taunt",
        AT_NAIR, "nair",
        AT_FAIR, "fair",
        AT_BAIR, "bair",
        AT_UAIR, "uair",
        AT_DAIR, "dair",
        AT_DATTACK, "dattack",
        AT_NSPECIAL, "nspecial",
        AT_FSPECIAL, "fspecial",
        AT_DSPECIAL_AIR, "dspecial_air",
        AT_USPECIAL, "uspecial"
    );""",
    depends=[data_structures.Map]
)

lib_get_current_sprite = Define(
    name="lib_get_current_sprite",
    version=0,
    docs="""\
    Gets the sprite corresponding to the `state` variable.
    Uses `lib_state_to_sprite_string` and `lib_attack_to_sprite_string`""",
    gml="""\
    var _current_state_string = lib_states_to_sprite_strings[?state]
    if (_current_state_string == undefined){
        var _current_attack_string = lib_attack_to_sprite_strings[?attack]
        return sprite_get(_current_attack_string)
    }
    return sprite_get(_current_state_string)""",
    depends=[lib_state_to_sprite_string, lib_attack_to_sprite_string]
)

DEPENDENCIES = [
    lib_state_to_sprite_string,
    lib_attack_to_sprite_string,

]
