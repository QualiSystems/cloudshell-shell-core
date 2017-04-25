import collections
import unittest

import mock

from cloudshell.shell.core.driver_utils import ExceptionMappingContext
from cloudshell.shell.core import exceptions


class TestExceptionMappingContext(unittest.TestCase):
    def setUp(self):
        self.logger = mock.MagicMock()
        self.exc_context = ExceptionMappingContext(logger=self.logger)

    def test__init__(self):
        """Check that method will correctly set '_exception_map' attribute"""
        exception_map = collections.OrderedDict([
            ("someException", "some exception message"),
            ("cloudshell.snmp.exceptions.SNMPConnectionFailed", "overridden message"),
        ])
        expected_exc_map = collections.OrderedDict([
            ('someException', 'some exception message'),
            ("cloudshell.snmp.exceptions.SNMPConnectionFailed", "overridden message"),
            ('cloudshell.cli.session_manager_impl.SessionManagerException', 'Failed to get CLI Session')])

        # act
        res = ExceptionMappingContext(logger=self.logger, exception_map=exception_map)
        # verify
        self.assertEqual(res._exception_map, expected_exc_map)

    def test_raise_exception_msg_is_not_none(self):
        """Check that method will raise ShellException exception with error message from the '_exception_map' attr"""
        exc_key = "SomeExceptionClass"
        expected_err_msg = "some exception message"
        self.exc_context._exception_map = {
            exc_key: expected_err_msg
        }

        with self.assertRaisesRegexp(exceptions.ShellException, expected_err_msg):
            self.exc_context._raise_shell_exception(exc_key=exc_key, exc_value="another exception message")

    def test_raise_exception_msg_is_none(self):
        """Check that method will raise ShellException exception with 'exc_value' argument as error message"""
        exc_key = "SomeExceptionClass"
        exc_value = "some exception message"
        self.exc_context._exception_map = {
            exc_key: None
        }

        with self.assertRaisesRegexp(exceptions.ShellException, exc_value):
            self.exc_context._raise_shell_exception(exc_key=exc_key, exc_value=exc_value)

    def test__enter__(self):
        """Check that method will return the same instance"""
        with self.exc_context as entered_context:
            self.assertEqual(self.exc_context, entered_context)

    def test__exit__exception_base_visible_exception(self):
        """Check that method will re-raise exception if it is an instance of BaseVisibleException"""
        exc_message = "some exception message"

        class SomeUserVisibleException(exceptions.BaseVisibleException):
            pass

        with self.assertRaisesRegexp(SomeUserVisibleException, exc_message):
            with self.exc_context:
                raise SomeUserVisibleException(exc_message)

    def test__exit__exception_class_in_map(self):
        """Check that method will call '_raise_shell_exception' if exception class is in '_exception_map' attr"""
        class SomeException(Exception):
            pass

        exc_message = "some exception message"
        self.exc_context._raise_shell_exception = mock.MagicMock(side_effect=exceptions.ShellException)

        self.exc_context._exception_map = {
            SomeException: "exception message for SomeException"
        }

        # act
        with self.assertRaises(exceptions.ShellException):
            with self.exc_context:
                exc = SomeException(exc_message)
                raise exc

        # verify
        self.exc_context._raise_shell_exception.assert_called_once_with(exc_key=SomeException,
                                                                        exc_value=exc)

    def test__exit__exception_class_path_in_map(self):
        """Check that method will call '_raise_shell_exception' if exception class path is in '_exception_map' attr"""
        class SomeException(Exception):
            pass

        exc_message = "some exception message"
        exc_class_path = "cloudshell.tests.test_utils.test_driver_utils.SomeException"
        self.exc_context._raise_shell_exception = mock.MagicMock(side_effect=exceptions.ShellException)

        self.exc_context._exception_map = {
            exc_class_path: "exception message for SomeException"
        }

        # act
        with self.assertRaises(exceptions.ShellException):
            with self.exc_context:
                exc = SomeException(exc_message)
                raise exc

        # verify
        self.exc_context._raise_shell_exception.assert_called_once_with(exc_key=exc_class_path,
                                                                        exc_value=exc)

    @unittest.skip("For now we will just re-raise all internal exceptions")
    def test__exit__exception_not_in_map(self):
        """Check that method will raise exceptions.ShellException if there is no such exception in the map"""
        exc_message = "some exception message"

        with self.assertRaisesRegexp(exceptions.ShellException, "Command failed. Please check logs for more details"):
            with self.exc_context:
                raise Exception(exc_message)
