from unittest import TestCase
from mock import MagicMock
from cloudshell.shell.core.api_utils import decrypt_password_from_attribute
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails


class TestApiUtils(TestCase):
    def test_decrypt_password_by_attribute_name(self):
        password = 'test_password'
        attribute_name = 'Password'
        context = ResourceCommandContext()
        context.resource = ResourceContextDetails()
        context.resource.attributes = {attribute_name: password}
        api = MagicMock()
        api.DecryptPassword.return_value.Value = password
        self.assertTrue(password == decrypt_password_from_attribute(api=api, context=context,
                                                                    password_attribute_name=attribute_name))

