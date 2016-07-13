import threading

import types
from cloudshell.core.logger.qs_logger import get_qs_logger, log_execution_info
from cloudshell.shell.core.context_utils import is_instance_of, get_reservation_context_attribute
import inject


@inject.params(context='context', config='config')
def get_logger_for_driver(context=None, config=None):
    """
        Create QS Logger for command context AutoLoadCommandContext, ResourceCommandContext
        or ResourceRemoteCommandContext
        :param context:
        :param config:
        :return:
    """
    if hasattr(config, 'HANDLER_CLASS'):
        handler_class = config.HANDLER_CLASS
    else:
        handler_class = None

    if handler_class and isinstance(handler_class, types.ClassType):
        logger_name = handler_class.__name__
    elif handler_class and isinstance(handler_class, str):
        logger_name = handler_class
    else:
        logger_name = 'QS'

    if is_instance_of(context, config.AUTOLOAD_COMMAND_CONTEXT):
        reservation_id = 'Autoload'
        resource_name = context.resource.name
    elif is_instance_of(context, config.RESOURCE_COMMAND_CONTEXT):
        reservation_id = context.reservation.reservation_id
        resource_name = context.resource.name
    elif is_instance_of(context, config.RESOURCE_REMOTE_COMMAND_CONTEXT):
        reservation_id = context.remote_reservation.reservation_id
        resource_name = context.remote_endpoints[0].name
    else:
        raise Exception('get_context_based_logger', 'Unsuppported command context provided {0}'.format(context))

    exec_info = get_execution_info(context)
    qs_logger = get_qs_logger(reservation_id, logger_name, resource_name)
    log_execution_info(qs_logger, exec_info)
    return qs_logger


def get_execution_info(context):
    """Aggregate information about execution server


    :param reservation: context.reservation info
    :param api: cloudshell.api session

    :return: dict with aggregated info
    """

    import platform, socket

    reservation_info = {}
    hostname = socket.gethostname()
    reservation_info['Python version'] = platform.python_version()
    reservation_info['Operating System'] = platform.platform()
    reservation_info['Platform'] = platform.system()
    reservation_info['Hostname'] = hostname
    reservation_info['IP'] = socket.gethostbyname(hostname)

    try:
        reservation_info['ReservationID'] = get_reservation_context_attribute('reservation_id', context)
        reservation_info['Description'] = get_reservation_context_attribute('description', context)
        reservation_info['EnviromentName'] = get_reservation_context_attribute('environment_name', context)
        reservation_info['Username'] = get_reservation_context_attribute('owner_user', context)
    except:
        pass

    return reservation_info


@inject.params(context='context', config='config')
def get_logger_with_thread_id(context=None, config=None):
    """
    Create QS Logger for command context AutoLoadCommandContext, ResourceCommandContext
    or ResourceRemoteCommandContext with thread name
    :param context:
    :param config:
    :return:
    """
    logger = get_logger_for_driver(context, config)
    child = logger.getChild(threading.currentThread().name)
    for handler in logger.handlers:
        child.addHandler(handler)
    child.level = logger.level
    for log_filter in logger.filters:
        child.addFilter(log_filter)
    return child
