from weakref import WeakKeyDictionary
from threading import currentThread

from cloudshell.configuration.cloudshell_shell_core_binding_keys import CONFIG, CONTEXT, API
import inject
from cloudshell.shell.core import context as driver_context
from abc import ABCMeta

_CONTEXT_CONTAINER = WeakKeyDictionary()


@inject.params(config=CONFIG)
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
    """Decorator which put context from function args to container"""

    def wrap_func(*args, **kwargs):
        module = driver_context
        for arg in list(args) + kwargs.values():
            if hasattr(arg, '__class__') and arg.__class__.__name__ in dir(module):
                put_context(arg)
                break
        return func(*args, **kwargs)

    return wrap_func


class ContextFromArgsMeta(ABCMeta):
    """Metaclass which decorate all driver methods by context_from_args decorator"""

    def __new__(metaclass, name, parents, attrs):
        decorated_attrs = {}
        for key, value in attrs.iteritems():
            if callable(value) and not key.startswith('_'):
                decorated_attrs[key] = context_from_args(value)
            else:
                decorated_attrs[key] = value
        return type.__new__(metaclass, name, parents, decorated_attrs)


@inject.params(context=CONTEXT)
def get_resource_context_details(context):
    """Helps to get resource context details"""
    if context and hasattr(context, 'resource'):
        return context.resource
    else:
        raise Exception('get_resource_context_details', 'Context does not have resource attribute')


@inject.params(context=CONTEXT)
def get_resource_context_attribute(attribute, context):
    """Helps to get resource context attribute"""
    resource = get_resource_context_details(context)
    if resource and hasattr(resource, attribute):
        return getattr(resource, attribute)
    else:
        raise Exception('get_resource_context_attribute',
                        'Resource context does not have attribute {0}'.format(attribute))


@inject.params(context=CONTEXT)
def get_attribute_by_name(attribute_name, context=None):
    """Return attribute from attributes or resource context """
    attributes = get_resource_context_attribute('attributes', context)
    resolved_attribute = None
    if attribute_name in attributes:
        resolved_attribute = attributes[attribute_name]
    return resolved_attribute


def get_attribute_by_name_wrapper(attribute):
    """Wrapper uses to closure get_attribute_by_name func"""

    def attribute_func():
        return get_attribute_by_name(attribute)

    return attribute_func


@inject.params(context=CONTEXT)
def get_resource_address(context):
    """Returns resource address"""
    return get_resource_context_attribute('address', context)


@inject.params(context=CONTEXT)
def get_resource_name(context):
    """Returns resource name"""
    return get_resource_context_attribute('name', context)


@inject.params(context=CONTEXT)
def get_reservation_context_details(context):
    """Helps to get reservation context details"""
    if context and hasattr(context, 'reservation'):
        reservation = context.reservation
    elif context and hasattr(context, 'remote_reservation'):
        reservation = context.remote_reservation
    else:
        raise Exception('get_reservation_context_details',
                        'Context does not have reservation or remote_reservation attribute')
    return reservation


@inject.params(context=CONTEXT)
def get_reservation_context_attribute(attribute, context):
    """Helps to get reservation context attribute"""
    reservation = get_reservation_context_details(context)
    if reservation and hasattr(reservation, attribute):
        return getattr(reservation, attribute)
    else:
        raise Exception('get_reservation_context_attribute',
                        'Reservation context does not have attribute {0}'.format(attribute))


@inject.params(context=CONTEXT)
def get_connectivity_context_details(context):
    """Helps to get connectivity context details"""
    if context and hasattr(context, 'connectivity'):
        return context.connectivity
    else:
        raise Exception('get_connectivity_context_details',
                        'Context does not have connectivity attribute')


@inject.params(context=CONTEXT)
def get_connectivity_context_attribute(attribute, context):
    """Helps to get connectivity context attribute"""
    connectivity = get_connectivity_context_details(context)
    if connectivity and hasattr(connectivity, attribute):
        return getattr(connectivity, attribute)
    else:
        raise Exception('get_connectivity_context_attribute',
                        'Connectivity context does not have attribute {0}'.format(attribute))


@inject.params(api=API)
def decrypt_password(password, api):
    """Uses api to decrypt password"""
    return api.DecryptPassword(password).Value


def get_decrypted_password_by_attribute_name_wrapper(attribute):
    """Wrapper func which gets password by attribute from context and decrypt it"""

    def attribute_func():
        password = get_attribute_by_name(attribute)
        return decrypt_password(password)

    return attribute_func
