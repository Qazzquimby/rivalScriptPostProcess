from script_process.dependencies import Init

lib_attacks = Init(
    name="lib_attacks",
    gml="""\
    [
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
    ];"""
)

lib_dodge_states = Init(
    name="lib_dodge_states",
    gml="""\
    [
        PS_AIR_DODGE,
        PS_ROLL_BACKWARD,
        PS_ROLL_FORWARD,
        PS_TECH_GROUND,
        PS_TECH_BACKWARD,
        PS_TECH_FORWARD,
        PS_WALL_TECH
    ];"""
)

DEPENDENCIES = [
    lib_attacks,
    lib_dodge_states,
]
