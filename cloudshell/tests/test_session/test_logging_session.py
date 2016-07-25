import os
from logging import Logger
from unittest import TestCase

from mock import mock

from cloudshell.shell.core.driver_context import AutoLoadCommandContext, ResourceContextDetails, ResourceCommandContext, \
    ResourceRemoteCommandContext, ReservationContextDetails
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.core.logger.qs_logger import _LOGGER_CONTAINER


class TestLoggingSessionContext(TestCase):
    def setUp(self):
        # Clear loggers between tests
        _LOGGER_CONTAINER.clear()

    def test_logger_initialized_for_autoload_context(self):
        # Arrange
        auto_load_context = mock.create_autospec(AutoLoadCommandContext)
        auto_load_context.resource = mock.create_autospec(ResourceContextDetails)
        auto_load_context.resource.name = 'my_device'

        # Act
        with LoggingSessionContext(auto_load_context) as logger:

            # Assert
            self.assertIsInstance(logger, Logger)
            base_filename = logger.handlers[0].baseFilename
            self.assertEqual(self._get_filename(base_filename), 'my_device')
            self.assertEqual(self._get_directory_name(base_filename), 'inventory')

    def test_logger_initialized_for_resource_context_without_reservation(self):
        # Arrange
        resource_command_context = mock.create_autospec(ResourceCommandContext)
        resource_command_context.resource = mock.create_autospec(ResourceContextDetails)
        resource_command_context.resource.name = 'my_device'
        resource_command_context.reservation = None

        # Act
        with LoggingSessionContext(resource_command_context) as logger:

            # Assert
            self.assertIsInstance(logger, Logger)
            base_filename = logger.handlers[0].baseFilename
            self.assertEqual(self._get_filename(base_filename), 'my_device')
            self.assertEqual(self._get_directory_name(base_filename), 'inventory')

    def test_logger_initialized_for_resource_context_with_reservation(self):
        # Arrange
        resource_command_context = mock.create_autospec(ResourceCommandContext)
        resource_command_context.resource = mock.create_autospec(ResourceContextDetails)
        resource_command_context.resource.name = 'my_device'
        resource_command_context.reservation = mock.create_autospec(ReservationContextDetails)
        resource_command_context.reservation.reservation_id = 'reservation_id1'

        # Act
        with LoggingSessionContext(resource_command_context) as logger:

            # Assert
            self.assertIsInstance(logger, Logger)
            base_filename = logger.handlers[0].baseFilename
            self.assertEqual(self._get_filename(base_filename), 'my_device')
            self.assertEqual(self._get_directory_name(base_filename), 'reservation_id1')

    def test_logger_initialized_for_remote_context_without_reservation(self):
        # Arrange
        remote_command_context = mock.create_autospec(ResourceRemoteCommandContext)
        remote_command_context.resource = mock.create_autospec(ResourceContextDetails)
        remote_command_context.resource.name = 'my_device'
        remote_command_context.remote_reservation = None
        remote_endpoint = mock.create_autospec(ResourceContextDetails)
        remote_endpoint.name = 'connected_device'
        remote_command_context.remote_endpoints = [remote_endpoint]

        # Act
        with LoggingSessionContext(remote_command_context) as logger:

            # Assert
            self.assertIsInstance(logger, Logger)
            base_filename = logger.handlers[0].baseFilename
            self.assertEqual(self._get_filename(base_filename), 'connected_device')
            self.assertEqual(self._get_directory_name(base_filename), 'inventory')

    def test_logger_initialized_for_remote_context_with_reservation(self):
        # Arrange
        remote_command_context = mock.create_autospec(ResourceRemoteCommandContext)
        remote_command_context.resource = mock.create_autospec(ResourceContextDetails)
        remote_command_context.resource.name = 'my_device'
        remote_command_context.remote_reservation = mock.create_autospec(ReservationContextDetails)
        remote_command_context.remote_reservation.reservation_id = 'reservation_id1'
        remote_endpoint = mock.create_autospec(ResourceContextDetails)
        remote_endpoint.name = 'connected_device'
        remote_command_context.remote_endpoints = [remote_endpoint]

        # Act
        with LoggingSessionContext(remote_command_context) as logger:

            # Assert
            self.assertIsInstance(logger, Logger)
            base_filename = logger.handlers[0].baseFilename
            self.assertEqual(self._get_filename(base_filename), 'connected_device')
            self.assertEqual(self._get_directory_name(base_filename), 'reservation_id1')

    @staticmethod
    def _get_directory_name(base_filename):
        return os.path.split(os.path.dirname(base_filename))[-1]

    @staticmethod
    def _get_filename(base_filename):
        return os.path.basename(base_filename).split('--')[0]



