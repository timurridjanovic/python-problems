#!/usr/local/bin/python

def insert_end_node(dct, node):
    if dct.get(node):
        dct[node] += 1
    else:
        dct[node] = 1
    return dct

def check_if_valid_types(dct, tpl):
    if not isinstance(dct, dict):
        raise TypeError('dct has to be a dictionary')
    if not isinstance(tpl, tuple):
        raise TypeError('tpl has to be a tuple')

def incr_dict(dct, tpl):
    check_if_valid_types(dct, tpl)

    if len(tpl) < 1:
        return dct

    start_node = tpl[0]
    end_node = tpl[-1]

    open_list = list(tpl)
    temp_dict = dct

    while len(open_list) > 0:
        current_node = open_list.pop(0)
        
        if current_node == end_node:
            temp_dict = insert_end_node(temp_dict, current_node)
            break
        
        exists = temp_dict.get(current_node)
        if not exists or isinstance(exists, int):
            temp_dict[current_node] = {}

        temp_dict = temp_dict[current_node]
        
    return dct
