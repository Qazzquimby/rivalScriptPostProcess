from script_process.dependencies import Define

create_list_if_not_exists = Define(
    name="create_list_if_not_exists",
    version=0,
    params=['_name'],
    docs="""\
    Create a list variable with the name if it does not already exist.""",
    gml="""\
    if _name not in self || !ds_list_valid(get(_name)){
        set(_name, ds_list_create())
    }"""
)

DEPENDENCIES = [
    create_list_if_not_exists
]
