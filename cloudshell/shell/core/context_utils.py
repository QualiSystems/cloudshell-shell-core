from weakref import WeakKeyDictionary
from threading import currentThread

import inject
from cloudshell.shell.core import context as driver_context
from cloudshell.shell.core.context import ResourceContextDetails
from abc import ABCMeta

_CONTEXT_CONTAINER = WeakKeyDictionary()


@inject.params(config='config')
def put_context(context_obj, config=None):
    if hasattr(config, 'CONTEXT_WRAPPER') and callable(config.CONTEXT_WRAPPER):
        suitable_context = config.CONTEXT_WRAPPER(context_obj)
    else:
        suitable_context = context_obj
    _CONTEXT_CONTAINER[currentThread()] = suitable_context


def get_context():
    if currentThread() in _CONTEXT_CONTAINER:
        return _CONTEXT_CONTAINER[currentThread()]
    return None


def is_instance_of(context, type_name):
    context_type = context.__class__.__name__
    return context_type == type_name


def build_suitable_context(context_obj):
    module = driver_context
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
        module = driver_context
        for arg in list(args) + kwargs.values():
            if hasattr(arg, '__class__') and arg.__class__.__name__ in dir(module):
                put_context(arg)
                break
        return func(*args, **kwargs)

    return wrap_func


class ContextFromArgsMeta(ABCMeta):
    def __new__(metaclass, name, parents, attrs):
        decorated_attrs = {}
        for key, value in attrs.iteritems():
            if callable(value) and not key.startswith('_'):
                decorated_attrs[key] = context_from_args(value)
            else:
                decorated_attrs[key] = value
        return type.__new__(metaclass, name, parents, decorated_attrs)


@inject.params(context='context')
def get_attribute_by_name(attribute_name, context=None):
    if context and hasattr(context, 'resource') and is_instance_of(context.resource, ResourceContextDetails.__name__):
        attributes = context.resource.attributes
        resolved_attribute = None
        if attribute_name in attributes:
            resolved_attribute = attributes[attribute_name]
        return resolved_attribute
    else:
        raise Exception('Wrong context supplied')


def get_attribute_by_name_wrapper(attribute):
    def attribute_func():
        return get_attribute_by_name(attribute)

    return attribute_func


@inject.params(context='context')
def get_resource_address(context):
    if context and hasattr(context, 'resource') and is_instance_of(context.resource, ResourceContextDetails.__name__):
        return context.resource.address
    else:
        raise Exception('get_resource_address', 'Context do not has resource')


@inject.params(context='context')
def get_resource_name(context):
    if context and hasattr(context, 'resource') and is_instance_of(context.resource, ResourceContextDetails.__name__):
        return context.resource.name
    else:
        raise Exception('get_resource_name', 'Context do not has resource')


@inject.params(api='api')
def decrypt_password(password, api):
    return api.DecryptPassword(password).Value


def get_decrypted_password_by_attribute_name_wrapper(attribute):
    def attribute_func():
        password = get_attribute_by_name(attribute)
        return decrypt_password(password)

    return attribute_func
