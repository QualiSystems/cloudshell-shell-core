import unittest
from unittest import TestCase
from mock import Mock

from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext


class TestCloudShellSessionContext(TestCase):

    @unittest.skip('import failure')
    def test_cloudshell_session_context_proper_initialized(self):
        context = Mock()
        with CloudShellSessionContext(context) as cloudshell_session_context:
            cloudshell_session = cloudshell_session_context.get_objects()
            self.assertIsInstance(cloudshell_session, CloudShellAPISession)
