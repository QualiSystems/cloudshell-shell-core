from __future__ import annotations

import platform
import socket

from cloudshell.logging.qs_logger import get_qs_logger

from cloudshell.shell.core.context_utils import (
    get_reservation_context_attribute,
    is_instance_of,
)
from cloudshell.shell.core.utils.get_installed_packages import get_installed_packages

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
    def get_execution_info(context) -> dict[str, dict[str, str | tuple[str]]]:
        """Aggregate information about execution server.

        :param context: ResourceCommandContext
        :return: dict with aggregated info
        """
        reservation_info = {}
        hostname = socket.gethostname()
        reservation_info["Python Version"] = platform.python_version()
        reservation_info["Operating System"] = platform.platform()
        reservation_info["Platform"] = platform.system()
        reservation_info["Hostname"] = hostname

        try:
            reservation_info["IP"] = socket.gethostbyname(hostname)
        except Exception:
            reservation_info["IP"] = "n/a"

        try:
            reservation_info["Reservation ID"] = get_reservation_context_attribute(
                "reservation_id", context
            )
            reservation_info["Description"] = get_reservation_context_attribute(
                "description", context
            )
            reservation_info["Environment Name"] = get_reservation_context_attribute(
                "environment_name", context
            )
            reservation_info["Username"] = get_reservation_context_attribute(
                "owner_user", context
            )
        except Exception:
            pass

        installed_packages = tuple(
            f"{name} == {version}"
            for name, version in sorted(get_installed_packages().items())
        )

        exec_info = {
            "INFO": reservation_info,
            "DEBUG": {"Installed Packages": installed_packages},
        }

        return exec_info

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
        exec_info = LoggingSessionContext.get_execution_info(context)
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
