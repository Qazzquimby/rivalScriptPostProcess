from script_process.dependencies import Define

set_state = Define(
    name="set_state",
    params=['_new_state'],
    version=0,
    docs="""\
    Sets the state to the given state and resets the state timer.""",
    gml="""\
        state = _new_state
        state_timer = 0""")

set_window = Define(
    name="set_window",
    params=['_new_window'],
    version=0,
    docs="""\
    Sets the window to the given state and resets the window timer.""",
    gml="""\
        window = _new_window
        window_timer = 0""")

DEPENDENCIES = [
    set_state,
    set_window
]
