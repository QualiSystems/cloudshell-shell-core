from unittest import TestCase
import mock
from mock import Mock, MagicMock

from cloudshell.shell.core.driver_context import ResourceContextDetails, ResourceCommandContext, \
    ReservationContextDetails, ConnectivityContext, ResourceRemoteCommandContext
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext


class TestCloudShellSessionContext(TestCase):

    def test_cloudshell_session_context_proper_initialized(self):

        # Arrange
        context = mock.create_autospec(ResourceCommandContext)
        context.connectivity = mock.create_autospec(ConnectivityContext)
        context.connectivity.server_address = 'localhost'
        context.connectivity.admin_auth_token = '123456789'
        context.resource = mock.create_autospec(ResourceContextDetails)
        context.resource.name = 'my_device'
        context.reservation = mock.create_autospec(ReservationContextDetails)
        context.reservation.domain = 'my_space'

        with mock.patch('cloudshell.shell.core.session.cloudshell_session.CloudShellAPISession') as cloudshell_api_session:
            expected_cloudshell_session = Mock()
            cloudshell_api_session.return_value = expected_cloudshell_session

            # Act
            with CloudShellSessionContext(context) as cloudshell_session:

                # Assert
                cloudshell_api_session.assert_called_with(domain='my_space',
                                                          host='localhost',
                                                          password=None,
                                                          token_id='123456789',
                                                          username=None)
                self.assertEqual(cloudshell_session, expected_cloudshell_session)

    def test_cloudshell_session_context_proper_initialized_using_https(self):

        # Arrange
        context = mock.create_autospec(ResourceCommandContext)
        context.connectivity = mock.create_autospec(ConnectivityContext)
        context.connectivity.server_address = 'localhost'
        context.connectivity.admin_auth_token = '123456789'
        context.connectivity.cloudshell_api_scheme = 'https'
        context.resource = mock.create_autospec(ResourceContextDetails)
        context.resource.name = 'my_device'
        context.reservation = mock.create_autospec(ReservationContextDetails)
        context.reservation.domain = 'my_space'

        with mock.patch('cloudshell.shell.core.session.cloudshell_session.CloudShellAPISession') as cloudshell_api_session:
            expected_cloudshell_session = Mock()
            cloudshell_api_session.return_value = expected_cloudshell_session

            # Act
            with CloudShellSessionContext(context) as cloudshell_session:

                # Assert
                cloudshell_api_session.assert_called_with(domain='my_space',
                                                          host='localhost',
                                                          password=None,
                                                          token_id='123456789',
                                                          cloudshell_api_scheme='https',
                                                          username=None)
                self.assertEqual(cloudshell_session, expected_cloudshell_session)

    def test_cloudshell_session_from_remote_command(self):
        # Arrange
        context = mock.create_autospec(ResourceRemoteCommandContext)
        context.connectivity = mock.create_autospec(ConnectivityContext)
        context.connectivity.server_address = 'localhost'
        context.connectivity.admin_auth_token = '123456789'
        context.resource = Mock()
        context.resource.name = 'my_device'
        context.remote_reservation = Mock()
        context.remote_reservation.domain = 'my_space'

        with mock.patch('cloudshell.shell.core.session.cloudshell_session.CloudShellAPISession') as cloudshell_api_session:
            expected_cloudshell_session = Mock()
            cloudshell_api_session.return_value = expected_cloudshell_session

            # Act
            with CloudShellSessionContext(context) as cloudshell_session:

                # Assert
                cloudshell_api_session.assert_called_with(domain='my_space',
                                                          host='localhost',
                                                          password=None,
                                                          token_id='123456789',
                                                          username=None)
                self.assertEqual(cloudshell_session, expected_cloudshell_session)

    def test_cloudshell_session_global_domain_used_when_outside_of_reservation(self):

        # Arrange
        context = mock.create_autospec(ResourceCommandContext)
        context.connectivity = mock.create_autospec(ConnectivityContext)
        context.connectivity.server_address = 'localhost'
        context.connectivity.admin_auth_token = '123456789'
        context.resource = mock.create_autospec(ResourceContextDetails)
        context.resource.name = 'my_device'
        context.reservation = None

        with mock.patch('cloudshell.shell.core.session.cloudshell_session.CloudShellAPISession') as cloudshell_api_session:
            expected_cloudshell_session = MagicMock()
            cloudshell_api_session.return_value = expected_cloudshell_session

            # Act
            with CloudShellSessionContext(context) as cloudshell_session:

                # Assert
                cloudshell_api_session.assert_called_with(domain='Global',
                                                          host='localhost',
                                                          password=None,
                                                          token_id='123456789',
                                                          username=None)

                self.assertEqual(cloudshell_session, expected_cloudshell_session)
