import textwrap

from script_process.dependencies import Define, make_dependency


def test_happy():
    sut = Define(
        name="name",
        version=0,
        docs="""\
        docs0
        docs1
        """,
        gml="""\
            gml0
            gml1
            """
    )
    assert sut.gml == textwrap.dedent("""\
    #define name // Version 0
        // docs0
        // docs1
    
        gml0
        gml1""")


def test_create():
    in_gml = textwrap.dedent("""\
    #define name // Version 0
        // docs0
        // docs1
    
        gml0
        gml1""")

    sut = make_dependency(in_gml)
    assert sut.gml == in_gml

def test_create_with_params():
    in_gml = textwrap.dedent("""\
    #define name(_param0, _param1) // Version 0
        // docs0
        // docs1
    
        gml0
        gml1""")

    sut = make_dependency(in_gml)
    assert sut.gml == in_gml

