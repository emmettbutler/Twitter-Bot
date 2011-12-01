def debug_log(fn):
    def wrapper_fn(*args, **kwargs):
        print args, kwargs
        return fn(*args, **kwargs)
    return wrapper_fn

cache = list()

def memoize(fn):
    def wrapper_fn(*args, **kwargs):
        cache.append(dict(Func=fn.__name__, Args=args, Kw=kwargs))
        print cache
        return fn(*args, **kwargs)
    return wrapper_fn

