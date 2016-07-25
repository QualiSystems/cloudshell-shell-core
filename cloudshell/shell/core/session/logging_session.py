from cloudshell.core.logger.qs_logger import get_qs_logger, log_execution_info

from cloudshell.shell.core.context_utils import is_instance_of
from cloudshell.shell.core.dependency_injection.context_based_logger import get_execution_info

INVENTORY = 'inventory'


class LoggingSessionContext(object):
    def __init__(self, context):
        """
        Initializes logger for context
        :param context: CommandContext
        """
        self.context = context

    def __enter__(self):
        """
        Initializes logger for the context
        :return: Logger
        :rtype: logging.Logger
        """
        return LoggingSessionContext.get_logger_for_context(self.context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called upon end of the context. Does nothing
        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return:
        """
        return False

    @staticmethod
    def get_logger_for_context(context):
        """
        Create logger for context
        :param context:
        :return: the logger object
        :rtype: logging.Logger
        """
        if is_instance_of(context, 'AutoLoadCommandContext'):
            log_group = INVENTORY
            resource_name = context.resource.name
        elif is_instance_of(context, 'ResourceCommandContext'):
            log_group = context.reservation.reservation_id if context.reservation else INVENTORY
            resource_name = context.resource.name
        elif is_instance_of(context, 'ResourceRemoteCommandContext'):
            log_group = context.remote_reservation.reservation_id if context.remote_reservation else INVENTORY
            resource_name = context.remote_endpoints[0].name
        else:
            raise Exception('get_logger_for_context', 'Unsupported command context provided {0}'.format(context))

        exec_info = get_execution_info(context)
        qs_logger = get_qs_logger(log_group=log_group, log_category='QS', log_file_prefix=resource_name)
        log_execution_info(qs_logger, exec_info)
        return qs_logger




