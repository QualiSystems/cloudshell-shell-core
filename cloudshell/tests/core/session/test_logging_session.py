from unittest import TestCase

from mock import Mock, MagicMock

from cloudshell.shell.core.session.logging_session import LoggingSessionContext


class TestLoggingSession(TestCase):

    def test_log_written_when_exception_occurs(self):
        context = Mock()
        logger = Mock()
        logger.error = MagicMock()
        try:
            with LoggingSessionContext(context=context, logger=logger):
                raise ValueError('some value error occurred')
        except ValueError:
            self.assertTrue(logger.error.called)

