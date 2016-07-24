from cloudshell.core.context.context_service import ContextBasedService
from cloudshell.core.logger.qs_logger import get_qs_logger, log_execution_info

from cloudshell.shell.core.dependency_injection.context_based_logger import get_execution_info
from cloudshell.shell.core.driver_context import AutoLoadCommandContext, ResourceCommandContext, \
    ResourceRemoteCommandContext

INVENTORY = 'inventory'


class LoggingSessionContext(ContextBasedService):
    def __init__(self, context):
        """
        Initializes logger for context
        :param context: CommandContext
        """
        self.context = context
        self.logger = LoggingSessionContext.get_logger_for_context(context)

    def context_started(self):
        return self.logger

    def context_ended(self, exc_type, exc_val, exc_tb):
        return self

    def get_objects(self):
        """
        Create logger for context
        :return: the logger object
        :rtype: logging.Logger
        """
        return self.logger

    @staticmethod
    def get_logger_for_context(context):
        """
        Create logger for context
        :param context:
        :return: the logger object
        :rtype: logging.Logger
        """
        if isinstance(context, AutoLoadCommandContext):
            log_group = INVENTORY
            resource_name = context.resource.name
        elif isinstance(context, ResourceCommandContext):
            log_group = context.reservation.reservation_id if context.reservation else INVENTORY
            resource_name = context.resource.name
        elif isinstance(context, ResourceRemoteCommandContext):
            log_group = context.reservation.reservation_id if context.reservation else INVENTORY
            resource_name = context.remote_endpoints[0].name
        else:
            raise Exception('get_logger_for_context', 'Unsupported command context provided {0}'.format(context))

        exec_info = get_execution_info(context)
        qs_logger = get_qs_logger(log_group=log_group, log_category='QS', log_file_prefix=resource_name)
        log_execution_info(qs_logger, exec_info)
        return qs_logger




