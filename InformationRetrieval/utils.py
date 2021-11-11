from flask import request


def genQuery():
    query = {}
    args = request.args
    for arg in args:
        query[arg] = args[arg]
    """
    Maybe there are some reformatting steps.
    """
    return query