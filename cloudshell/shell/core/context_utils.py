from weakref import WeakKeyDictionary
from threading import currentThread


_CONTEXT_CONTAINER = WeakKeyDictionary()


def put_context(context_obj):
    _CONTEXT_CONTAINER[currentThread()] = context_obj


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

    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    attributes = get_resource_context_attribute(context=context, attribute='attributes')
    resolved_attribute = None
    if attribute_name in attributes:
        resolved_attribute = attributes[attribute_name]
    return resolved_attribute


def get_resource_address(context=None):
    """Returns resource address"""

    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    return get_resource_context_attribute(context=context, attribute='address')


def get_resource_name(context=None):
    """Returns resource name"""

    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
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
    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
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
    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    connectivity = get_connectivity_context_details(context)
    if connectivity and hasattr(connectivity, attribute):
        return getattr(connectivity, attribute)
    else:
        raise Exception('get_connectivity_context_attribute',
                        'Connectivity context does not have attribute {0}'.format(attribute))


def decrypt_password(api, password):
    """Uses api to decrypt password"""
    return api.DecryptPassword(password).Value

def decrypt_password_from_attribute(api, password_attribute_name, context=None):
    """Uses api to decrypt password"""
    if not context:
        _CONTEXT_CONTAINER.get(currentThread(), None)
    password = get_attribute_by_name(password_attribute_name, context)
    return api.DecryptPassword(password).Value
