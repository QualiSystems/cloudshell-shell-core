from weakref import WeakKeyDictionary
from threading import currentThread
from cloudshell.shell.core import driver_context

_CONTEXT_CONTAINER = WeakKeyDictionary()


def get_context():
    if currentThread() in _CONTEXT_CONTAINER:
        return _CONTEXT_CONTAINER[currentThread()]
    return None


def get_attribute_by_name_wrapper(attribute):
    """Wrapper uses to closure get_attribute_by_name func"""

    def attribute_func():
        return get_attribute_by_name(attribute)

    return attribute_func


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


def put_context(context):
    if context:
        _CONTEXT_CONTAINER[currentThread()] = context
    else:
        raise Exception('put_context', 'Context is None')


def get_resource_context_details(context=None):
    """Helps to get resource context details"""

    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    if context and hasattr(context, 'resource'):
        return context.resource
    else:
        raise Exception('get_resource_context_details', 'Context does not have resource attribute')


def is_instance_of(context, type_name):
    context_type = context.__class__.__name__
    return context_type == type_name


def get_resource_context_attribute(attribute, context=None):
    """Helps to get resource context attribute"""

    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    resource = get_resource_context_details(context)
    if resource and hasattr(resource, attribute):
        return getattr(resource, attribute)
    else:
        raise Exception('get_resource_context_attribute',
                        'Resource context does not have attribute {0}'.format(attribute))


def get_attribute_by_name(attribute_name, context=None):
    """Return attribute from attributes or resource context """

    attributes = get_resource_context_attribute(context=context, attribute='attributes')
    resolved_attribute = None
    if attribute_name in attributes:
        resolved_attribute = attributes[attribute_name]
    return resolved_attribute


def get_resource_address(context=None):
    """Returns resource address"""

    return get_resource_context_attribute(context=context, attribute='address')


def get_resource_name(context=None):
    """Returns resource name"""

    return get_resource_context_attribute(context=context, attribute='name')


def get_reservation_context_details(context=None):
    """Helps to get reservation context details"""

    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    if context and hasattr(context, 'reservation'):
        reservation = context.reservation
    elif context and hasattr(context, 'remote_reservation'):
        reservation = context.remote_reservation
    else:
        raise Exception('get_reservation_context_details',
                        'Context does not have reservation or remote_reservation attribute')
    return reservation


def get_reservation_context_attribute(attribute, context=None):
    """Helps to get reservation context attribute"""

    reservation = get_reservation_context_details(context)
    if reservation and hasattr(reservation, attribute):
        return getattr(reservation, attribute)
    else:
        raise Exception('get_reservation_context_attribute',
                        'Reservation context does not have attribute {0}'.format(attribute))


def get_connectivity_context_details(context=None):
    """Helps to get connectivity context details"""
    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    if context and hasattr(context, 'connectivity'):
        return context.connectivity
    else:
        raise Exception('get_connectivity_context_details',
                        'Context does not have connectivity attribute')


def get_connectivity_context_attribute(attribute, context=None):
    """Helps to get connectivity context attribute"""

    connectivity = get_connectivity_context_details(context)
    if connectivity and hasattr(connectivity, attribute):
        return getattr(connectivity, attribute)
    else:
        raise Exception('get_connectivity_context_attribute',
                        'Connectivity context does not have attribute {0}'.format(attribute))
