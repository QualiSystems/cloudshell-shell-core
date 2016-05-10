import types
from cloudshell.core.logger.qs_logger import get_qs_logger
from cloudshell.shell.core.context.context_utils import is_instance_of
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

    return get_qs_logger(reservation_id, logger_name, resource_name)
