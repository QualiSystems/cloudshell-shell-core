from __future__ import annotations

from cloudshell.logging.qs_logger import get_qs_logger

from cloudshell.shell.core.context_utils import is_instance_of
from cloudshell.shell.core.utils import get_execution_info

INVENTORY = "inventory"
DELETE_ARTIFACTS = "DeleteArtifacts"


class LoggingSessionContext:
    def __init__(self, context):
        """Initializes logger for context.

        :param context: CommandContext
        """
        self.context = context
        self._logger = None

    @staticmethod
    def get_logger_for_context(context):
        """Create logger for context.

        :param context:
        :return: the logger object
        :rtype: logging.Logger
        """
        if is_instance_of(context, "AutoLoadCommandContext"):
            log_group = INVENTORY
        elif is_instance_of(context, "ResourceCommandContext"):
            log_group = (
                context.reservation.reservation_id if context.reservation else INVENTORY
            )
        elif is_instance_of(context, "ResourceRemoteCommandContext"):
            log_group = (
                context.remote_reservation.reservation_id
                if context.remote_reservation
                else INVENTORY
            )
        elif is_instance_of(context, "UnreservedResourceCommandContext"):
            log_group = DELETE_ARTIFACTS
        else:
            raise Exception(
                "get_logger_for_context",
                f"Unsupported command context provided {context}",
            )

        resource_name = context.resource.name
        exec_info = get_execution_info(context)
        qs_logger = get_qs_logger(
            log_group=log_group,
            log_category="cloudshell",
            log_file_prefix=resource_name,
            exec_info=exec_info,
        )
        return qs_logger

    @staticmethod
    def get_logger_with_thread_id(context):
        """Create QS Logger for command context with thread name.

        Context can be: AutoLoadCommandContext, ResourceCommandContext
            or ResourceRemoteCommandContext
        :param context:
        :rtype: logging.Logger
        """
        logger = LoggingSessionContext.get_logger_for_context(context)
        return logger

    def __enter__(self):
        """Initializes logger for the context.

        :return: Logger
        :rtype: logging.Logger
        """
        self._logger = self.get_logger_with_thread_id(self.context)
        return self._logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called upon end of the context.

        Logs an error if exists
        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return:
        """
        if exc_val:
            self._logger.exception("Error occurred")
        return False
