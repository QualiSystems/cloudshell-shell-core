import os
import sys
from unittest import TestCase

from cloudshell.logging.qs_logger import _LOGGER_CONTAINER

from cloudshell.shell.core.driver_context import (
    AutoLoadCommandContext,
    ReservationContextDetails,
    ResourceCommandContext,
    ResourceContextDetails,
    ResourceRemoteCommandContext,
)
from cloudshell.shell.core.session.logging_session import (
    INVENTORY,
    LoggingSessionContext,
)

if sys.version_info >= (3, 0):
    from unittest import mock
else:
    import mock


class TestLoggingSessionContext(TestCase):
    def setUp(self):
        # Clear loggers between tests
        _LOGGER_CONTAINER.clear()

    @mock.patch("cloudshell.shell.core.session.logging_session.get_qs_logger")
    @mock.patch("cloudshell.shell.core.session.logging_session.log_execution_info")
    @mock.patch(
        "cloudshell.shell.core.session.logging_session.LoggingSessionContext"
        ".get_execution_info"
    )
    def test_logger_initialized_for_autoload_context(
        self, get_execution_info, log_execution_info, get_qs_logger
    ):
        # Arrange
        auto_load_context = mock.create_autospec(AutoLoadCommandContext)
        auto_load_context.resource = mock.create_autospec(ResourceContextDetails)
        auto_load_context.resource.name = "my_device"

        execution_info = mock.Mock()
        get_execution_info.return_value = execution_info

        qs_logger = mock.Mock()
        child_logger = mock.Mock()
        qs_logger.getChild.return_value = child_logger
        qs_logger.handlers = [mock.Mock()]
        qs_logger.filters = [mock.Mock()]
        get_qs_logger.return_value = qs_logger

        # Act
        with LoggingSessionContext(auto_load_context) as logger:
            get_execution_info.assert_called_once_with(auto_load_context)
            get_qs_logger.assert_called_once_with(
                log_group=INVENTORY,
                log_category="QS",
                log_file_prefix=auto_load_context.resource.name,
            )
            log_execution_info.assert_called_once_with(qs_logger, execution_info)
            self.assertEqual(child_logger, logger)

    @mock.patch("cloudshell.shell.core.session.logging_session.get_qs_logger")
    @mock.patch("cloudshell.shell.core.session.logging_session.log_execution_info")
    @mock.patch(
        "cloudshell.shell.core.session.logging_session.LoggingSessionContext"
        ".get_execution_info"
    )
    def test_logger_initialized_for_resource_context_without_reservation(
        self, get_execution_info, log_execution_info, get_qs_logger
    ):
        # Arrange
        resource_command_context = mock.create_autospec(ResourceCommandContext)
        resource_command_context.resource = mock.create_autospec(ResourceContextDetails)
        resource_command_context.resource.name = "my_device"
        resource_command_context.reservation = None

        execution_info = mock.Mock()
        get_execution_info.return_value = execution_info

        qs_logger = mock.Mock()
        child_logger = mock.Mock()
        qs_logger.getChild.return_value = child_logger
        qs_logger.handlers = [mock.Mock()]
        qs_logger.filters = [mock.Mock()]
        get_qs_logger.return_value = qs_logger

        # Act
        with LoggingSessionContext(resource_command_context) as logger:
            # Assert
            get_execution_info.assert_called_once_with(resource_command_context)
            get_qs_logger.assert_called_once_with(
                log_group=INVENTORY,
                log_category="QS",
                log_file_prefix=resource_command_context.resource.name,
            )
            log_execution_info.assert_called_once_with(qs_logger, execution_info)
            self.assertEqual(child_logger, logger)

    @mock.patch("cloudshell.shell.core.session.logging_session.get_qs_logger")
    @mock.patch("cloudshell.shell.core.session.logging_session.log_execution_info")
    @mock.patch(
        "cloudshell.shell.core.session.logging_session.LoggingSessionContext"
        ".get_execution_info"
    )
    def test_logger_initialized_for_resource_context_with_reservation(
        self, get_execution_info, log_execution_info, get_qs_logger
    ):
        # Arrange
        resource_command_context = mock.create_autospec(ResourceCommandContext)
        resource_command_context.resource = mock.create_autospec(ResourceContextDetails)
        resource_command_context.resource.name = "my_device"
        resource_command_context.reservation = mock.create_autospec(
            ReservationContextDetails
        )
        resource_command_context.reservation.reservation_id = "reservation_id1"

        reservation_id = mock.Mock()
        resource_command_context.reservation.reservation_id = reservation_id

        execution_info = mock.Mock()
        get_execution_info.return_value = execution_info

        qs_logger = mock.Mock()
        child_logger = mock.Mock()
        qs_logger.getChild.return_value = child_logger
        qs_logger.handlers = [mock.Mock()]
        qs_logger.filters = [mock.Mock()]
        get_qs_logger.return_value = qs_logger

        # Act
        with LoggingSessionContext(resource_command_context) as logger:
            # Assert
            get_execution_info.assert_called_once_with(resource_command_context)
            get_qs_logger.assert_called_once_with(
                log_group=reservation_id,
                log_category="QS",
                log_file_prefix=resource_command_context.resource.name,
            )
            log_execution_info.assert_called_once_with(qs_logger, execution_info)
            self.assertEqual(child_logger, logger)

    @mock.patch("cloudshell.shell.core.session.logging_session.get_qs_logger")
    @mock.patch("cloudshell.shell.core.session.logging_session.log_execution_info")
    @mock.patch(
        "cloudshell.shell.core.session.logging_session.LoggingSessionContext"
        ".get_execution_info"
    )
    def test_logger_initialized_for_remote_context_without_reservation(
        self, get_execution_info, log_execution_info, get_qs_logger
    ):
        # Arrange
        remote_command_context = mock.create_autospec(ResourceRemoteCommandContext)
        remote_command_context.resource = mock.create_autospec(ResourceContextDetails)
        remote_command_context.resource.name = "my_device"
        remote_command_context.remote_reservation = None
        remote_endpoint = mock.create_autospec(ResourceContextDetails)
        remote_endpoint.name = "connected_device"
        remote_command_context.remote_endpoints = [remote_endpoint]

        execution_info = mock.Mock()
        get_execution_info.return_value = execution_info

        qs_logger = mock.Mock()
        child_logger = mock.Mock()
        qs_logger.getChild.return_value = child_logger
        qs_logger.handlers = [mock.Mock()]
        qs_logger.filters = [mock.Mock()]
        get_qs_logger.return_value = qs_logger

        # Act
        with LoggingSessionContext(remote_command_context) as logger:
            # Assert
            get_execution_info.assert_called_once_with(remote_command_context)
            get_qs_logger.assert_called_once_with(
                log_group=INVENTORY,
                log_category="QS",
                log_file_prefix=remote_endpoint.name,
            )
            log_execution_info.assert_called_once_with(qs_logger, execution_info)
            self.assertEqual(child_logger, logger)

    @mock.patch("cloudshell.shell.core.session.logging_session.get_qs_logger")
    @mock.patch("cloudshell.shell.core.session.logging_session.log_execution_info")
    @mock.patch(
        "cloudshell.shell.core.session.logging_session.LoggingSessionContext"
        ".get_execution_info"
    )
    def test_logger_initialized_for_remote_context_with_reservation(
        self, get_execution_info, log_execution_info, get_qs_logger
    ):
        # Arrange
        remote_command_context = mock.create_autospec(ResourceRemoteCommandContext)
        remote_command_context.resource = mock.create_autospec(ResourceContextDetails)
        remote_command_context.resource.name = "my_device"
        remote_command_context.remote_reservation = mock.create_autospec(
            ReservationContextDetails
        )
        remote_command_context.remote_reservation.reservation_id = "reservation_id1"
        remote_endpoint = mock.create_autospec(ResourceContextDetails)
        remote_endpoint.name = "connected_device"
        remote_command_context.remote_endpoints = [remote_endpoint]

        execution_info = mock.Mock()
        get_execution_info.return_value = execution_info

        qs_logger = mock.Mock()
        child_logger = mock.Mock()
        qs_logger.getChild.return_value = child_logger
        qs_logger.handlers = [mock.Mock()]
        qs_logger.filters = [mock.Mock()]
        get_qs_logger.return_value = qs_logger

        # Act
        with LoggingSessionContext(remote_command_context) as logger:
            # Assert
            get_execution_info.assert_called_once_with(remote_command_context)
            get_qs_logger.assert_called_once_with(
                log_group=remote_command_context.remote_reservation.reservation_id,
                log_category="QS",
                log_file_prefix=remote_endpoint.name,
            )
            log_execution_info.assert_called_once_with(qs_logger, execution_info)
            self.assertEqual(child_logger, logger)

    @mock.patch("cloudshell.shell.core.session.logging_session.socket.gethostbyname")
    def test_get_execution_info_handles_gethostbyname_exception(
        self, get_host_by_name_mock
    ):
        # Arrange
        auto_load_context = mock.create_autospec(AutoLoadCommandContext)
        auto_load_context.resource = mock.create_autospec(ResourceContextDetails)
        auto_load_context.resource.name = "my_device"
        get_host_by_name_mock.side_effect = Exception("error")

        # Act
        result = LoggingSessionContext.get_execution_info(auto_load_context)

        self.assertEqual(result["IP"], "n/a")

    @staticmethod
    def _get_directory_name(base_filename):
        return os.path.split(os.path.dirname(base_filename))[-1]

    @staticmethod
    def _get_filename(base_filename):
        return os.path.basename(base_filename).split("--")[0]
