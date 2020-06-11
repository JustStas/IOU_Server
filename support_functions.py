import ast

def str_to_list(s):
    try:
        l = ast.literal_eval(s)
        l = [n.strip() for n in l]
    except ValueError:
        return 'ERROR'
    return l