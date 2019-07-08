from random import Random


# copied from six
def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def random_shuffle_algorithm(objs, ran=Random()):
    # ran.shuffle(objs)
    count = len(objs)
    for idx in range(count - 1):  # noqa
        other = ran.randrange(idx, count)
        objs[idx], objs[other] = objs[other], objs[idx]
    objs[:] = objs[::3] + objs[1::3] + objs[2::3]
