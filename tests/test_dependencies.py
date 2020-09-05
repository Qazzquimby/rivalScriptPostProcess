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


def test_create_with_no_version_given():
    in_gml = textwrap.dedent("""\
    #define name
        // docs0
        // docs1
    
        gml0
        gml1""")

    out_gml = textwrap.dedent("""\
        #define name // Version 0
            // docs0
            // docs1
        
            gml0
            gml1""")

    sut = make_dependency(in_gml)
    assert sut.gml == out_gml


def test_create_with_dependency():
    print_define = Define(
        name="print",
        version=0,
        docs="""\
            Prints each parameter to console, separated by spaces.""",
        gml="""\
            var _out_string = ""
            for (var i = 0; i < argument_count; i++){
                _out_string += string(argument[i])
                _out_string += " "
            }
            print_debug(_out_string)""")
    depends = [
        print_define
    ]

    in_gml = textwrap.dedent("""\
    #define name
        // docs0
        // docs1
    
        gml0
        print("blah")
        gml1""")

    sut = make_dependency(in_gml, depends)
    assert print_define in sut.depends
