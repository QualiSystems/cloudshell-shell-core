from weakref import WeakKeyDictionary
from threading import currentThread
import importlib

from cloudshell.shell.core.context import InitCommandContext

CONTEXT_CONTAINER = WeakKeyDictionary()


def put_context(context_obj):
    CONTEXT_CONTAINER[currentThread()] = build_suitable_context(context_obj)


def get_context():
    if currentThread() in CONTEXT_CONTAINER:
        return CONTEXT_CONTAINER[currentThread()]
    return None


def build_suitable_context(context_obj):
    module = importlib.import_module(InitCommandContext.__module__)
    context_class = context_obj.__class__.__name__
    if context_class in dir(module):
        classobject = getattr(module, context_class)
    else:
        raise Exception('build_suitable_context', 'Cannot find suitable context class')
    obj = classobject()
    for attribute in filter(lambda x: not str(x).startswith('__') and not x == 'ATTRIBUTE_MAP', dir(context_obj)):
        value = getattr(context_obj, attribute)
        if value and hasattr(value, '__class__') and value.__class__.__name__ in dir(module):
            value = build_suitable_context(value)

        if attribute in obj.ATTRIBUTE_MAP:
            obj_attr = obj.ATTRIBUTE_MAP[attribute]
        else:
            obj_attr = attribute

        setattr(obj, obj_attr, value)
    return obj


def context_from_args(func):
    def wrap_func(*args, **kwargs):
        module = importlib.import_module(InitCommandContext.__module__)
        for arg in list(args)+kwargs.values():
            if hasattr(arg, '__class__') and arg.__class__.__name__ in dir(module):
                put_context(arg)
                break
        return func(*args, **kwargs)

    return wrap_func
