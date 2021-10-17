

def do_nothing(value:any) -> any:
    return value 

def find_first(names:list, kwargs:dict, default:any = None, returnFunc:callable = do_nothing) -> any:
    """returns the first value from kwargs found by iterating the names list.  If not found, returns None.

    Args:
        names (list): names of possible keys in the kwargs
        kwargs (dict): dictionary of name/value pairs which will be examined
        default (any, optional): default to use if no name is found. Defaults to None.
        returnFunc (callable, optional): default to use if no name is found. Defaults to None.

    Returns:
        any: the value of the first name found in names, from the kwargs.  In not found, returns None.
    """
    for name in names:
        if name in kwargs:
            return returnFunc(kwargs[name])
    return returnFunc(default)

