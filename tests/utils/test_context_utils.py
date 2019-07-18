#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from unittest import TestCase

from cloudshell.shell.core.context_utils import (
    get_attribute_by_name,
    get_connectivity_context_attribute,
    get_context,
    get_reservation_context_attribute,
    get_resource_address,
    get_resource_name,
    put_context,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, patch
else:
    from mock import MagicMock, patch


class TestContextUtils(TestCase):
    def setUp(self):
        self.context = MagicMock()

    def test_put_and_get_context(self):
        put_context(self.context)
        self.assertEqual(self.context, get_context())

    def test_put_context_raises_exception(self):
        context = None
        with self.assertRaises(Exception):
            put_context(context)

    def test_get_attribute_by_name(self):
        attribute_name = "test_attribute"
        attribute_value = "value"
        self.context.resource.attributes = {attribute_name: attribute_value}
        self.assertEqual(
            attribute_value,
            get_attribute_by_name(context=self.context, attribute_name=attribute_name),
        )

    def test_get_resource_address(self):
        resource_address = "address"
        self.context.resource.address = resource_address
        self.assertEqual(resource_address, get_resource_address(context=self.context))

    def test_get_resource_name(self):
        resource_name = "resource_name"
        self.context.resource.name = resource_name
        self.assertEqual(resource_name, get_resource_name(context=self.context))

    def test_get_reservation_context_attribute(self):
        domain = "domain_name"
        self.context.reservation.domain = domain
        self.assertEqual(
            domain, get_reservation_context_attribute("domain", self.context)
        )

    @patch(
        "cloudshell.shell.core.context_utils.get_reservation_context_details",
        new=MagicMock(return_value=None),
    )
    def test_get_reservation_context_attribute_exception(self):
        domain = "domain_name"
        self.context.reservation.domain = domain
        with self.assertRaises(Exception):
            get_reservation_context_attribute("domain", self.context)

    def test_get_connectivity_context_attribute(self):
        server_address = "server_address"
        self.context.connectivity.server_address = server_address
        self.assertEqual(
            server_address,
            get_connectivity_context_attribute("server_address", self.context),
        )

    @patch(
        "cloudshell.shell.core.context_utils.get_connectivity_context_details",
        new=MagicMock(return_value=None),
    )
    def test_get_connectivity_context_attribute_exception(self):

        server_address = "server_address"
        self.context.connectivity.server_address = server_address
        with self.assertRaises(Exception):
            get_connectivity_context_attribute("server_address", self.context)
