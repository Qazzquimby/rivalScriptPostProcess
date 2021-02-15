from script_process.dependencies import Define

damage_object = Define(
    name="damage_object",
    version=0,
    params=['_target', '_amount'],
    docs="""\
    Deals the amount of damage to the target. Works on articles that have a `damage` field.""",
    gml="""\
    if _target.object_index == oPlayer{
        var player_number = get_instance_player(_target)
        take_damage(player_number, -1, _amount);
    } else {
        if (variable_instance_exists(_target, 'damage')){
            _target.damage += _amount;
        }
    }"""
)

DEPENDENCIES = [
    damage_object
]