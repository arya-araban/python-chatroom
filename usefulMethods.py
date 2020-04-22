def change_inside_tuple_value(initial_tuple, index, value):
    lst = list(initial_tuple)
    lst[index] = value
    return tuple(lst)
