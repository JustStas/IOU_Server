import ast

def str_to_list(s):
    l = ast.literal_eval(s)
    l = [n.strip() for n in l]
    return l