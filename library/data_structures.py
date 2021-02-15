from script_process.dependencies import Define

Array = Define(
    name="Array",
    version=0,
    docs="""\
    ...args
    Unpacks the arguments into a new array.
    """,
    gml="""\
    var arr = array_create(argument_count, undefined);
    for (var i=0; i<argument_count; i+=1){
        arr[i] = argument[i];
    }
    return arr;
    """
)

Array_from_list = Define(
    name="Array_from_list",
    version=0,
    params=['list'],
    docs="""\
    Creates a new array from the contents of the list. Does not destroy the list.""",
    gml="""\
    var arr = array_create(ds_list_size(list), undefined);
    for (var i=0; i<ds_list_size(list); i+=1){
        arr[i] = list[|i];
    }
    return arr;
    """
)

Map = Define(
    name="Map",
    version=0,
    docs="""\
    Creates a mapping from each pair of arguments.
    See https://docs.yoyogames.com/source/dadiospice/002_reference/data%20structures/ds%20maps/index.html
    my_map = Map(
        "a", 1,
        "b", 2,
    )
    my_map[?"a"]
    >>> 1
    """,
    gml="""\
    if (argument_count mod 2 != 0) {
        print_debug(`Expected an even number of arguments, got ${string(argument_count)}.`);
    }
    var _map = ds_map_create();
    for (var i = 0; i < argument_count; i += 2) {
        _map[? argument[i]] = argument[i+1];
    }
    return _map;
    """)

List = Define(
    name="List",
    version=0,
    docs="""\
    Creates an list of the arguments. 
    See https://docs.yoyogames.com/source/dadiospice/002_reference/data%20structures/ds%20lists/
    my_list = List(
        1,
        2,
    )
    my_list[|0]
    >>> 1
    """,
    gml="""\
    var list = ds_list_create();
    for (var i = 0; i < argument_count; i++) {
      ds_list_add(list, argument[i]);
    }
    return list;
    """
)

Stack = Define(
    name="Stack",
    version=0,
    docs="""\
    Adds the arguments to the stack from top to bottom (first argument is on top)
    See https://docs.yoyogames.com/source/dadiospice/002_reference/data%20structures/ds%20stacks/index.html
    my_stack = Stack(
        1,
        2,
    )
    ds_stack_pop(my_stack)
    >>> 1
    """,
    gml="""\
    var stack = ds_stack_create();
    for (var i = argument_count-1; i >= 0; i--) {
        ds_stack_push(stack, argument[i]);
    }
    return stack;
    """
)

Queue = Define(
    name="Queue",
    version=0,
    docs="""\
    Adds the arguments to the stack in order
    See https://docs.yoyogames.com/source/dadiospice/002_reference/data%20structures/ds%20queues/index.html
    my_queue = Queue(
        1,
        2,
    )
    ds_queue_dequeue(my_queue)
    >>> 2
    """,
    gml="""\
    var queue = ds_queue_create();
    for (var i = 0; i < argument_count; i++) {
      ds_queue_enqueue(queue, argument[i]);
    }
    return queue;
    """
)

DEPENDENCIES = [
    Map,
    List,
    Stack,
    Queue
]
