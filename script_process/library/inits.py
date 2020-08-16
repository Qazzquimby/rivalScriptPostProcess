from script_process.dependencies import Init

make_attack = Init(
    name="lib_attacks",
    docs="""\
    Lists attack IDs.
    """,
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
        ]"""
)
