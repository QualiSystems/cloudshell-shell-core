import types
from cloudshell.core.logger.qs_logger import get_qs_logger
import inject
from cloudshell.shell.core.context import AutoLoadCommandContext, ResourceCommandContext, ResourceRemoteCommandContext


@inject.params(context='context', handler_class='handler_class')
def get_logger_for_driver(context=None, handler_class=None):
    """
        Create QS Logger for command context AutoLoadCommandContext, ResourceCommandContext
        or ResourceRemoteCommandContext
        :param context:
        :param handler_class:
        :return:
    """

    if handler_class and isinstance(handler_class, types.ClassType):
        logger_name = handler_class.__name__
    elif handler_class and isinstance(handler_class, str):
        logger_name = handler_class
    else:
        logger_name = 'QS'

    if isinstance(context, AutoLoadCommandContext):
        reservation_id = 'Autoload'
        resource_name = context.resource.name
    elif isinstance(context, ResourceCommandContext):
        reservation_id = context.reservation.reservation_id
        resource_name = context.resource.name
    elif isinstance(context, ResourceRemoteCommandContext):
        reservation_id = context.remote_reservation.reservation_id
        resource_name = context.remote_endpoints[0].name
    else:
        raise Exception('get_context_based_logger', 'Unsuppported command context provided {0}'.format(context))

    return get_qs_logger(reservation_id, logger_name, resource_name)

