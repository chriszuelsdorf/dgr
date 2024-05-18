class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def convert_to_dotdict(o):
    if type(o) == dict:
        return DotDict({k:convert_to_dotdict(v) for k, v in o.items()})
    elif type(o) == list:
        return [convert_to_dotdict(x) for x in o]
    return o
