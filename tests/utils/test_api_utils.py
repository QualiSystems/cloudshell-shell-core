#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from unittest import TestCase

from cloudshell.shell.core.api_utils import decrypt_password_from_attribute

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestApiUtils(TestCase):
    def setUp(self):
        self.context = MagicMock()

    def test_decrypt_password_by_attribute_name(self):
        password = "test_password"
        attribute_name = "Password"

        api = MagicMock()
        self.context.resource.attributes = {attribute_name: password}

        api.DecryptPassword.return_value.Value = password
        self.assertEqual(
            password,
            decrypt_password_from_attribute(
                api=api, context=self.context, password_attribute_name=attribute_name
            ),
        )
