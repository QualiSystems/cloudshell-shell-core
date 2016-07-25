from unittest import TestCase

from mock import Mock, mock

from cloudshell.shell.core.driver_context import ResourceContextDetails, ResourceCommandContext, \
    ReservationContextDetails, ConnectivityContext
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
        context.reservation.domain = 'global'

        with mock.patch('cloudshell.shell.core.session.cloudshell_session.CloudShellAPISession') as cloudshell_api_session:
            expected_cloudshell_session = Mock()
            cloudshell_api_session.return_value = expected_cloudshell_session

            # Act
            with CloudShellSessionContext(context) as cloudshell_session:

                # Assert
                self.assertEqual(cloudshell_session, expected_cloudshell_session)
