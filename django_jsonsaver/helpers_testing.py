import inspect


def get_decorators(function):
    """Returns list of decorator names used in a given function."""
    source = inspect.getsource(function)
    index = source.find("def ")
    return [
        line.strip().split()[0]
        for line in source[:index].strip().splitlines()
        if line.strip()[0] == "@"
    ]
