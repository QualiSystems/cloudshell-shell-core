from unittest import TestCase
from mock import MagicMock
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails, \
    ConnectivityContext
from cloudshell.shell.core.context_utils import put_context, get_context, get_attribute_by_name, get_resource_address, \
    get_reservation_context_attribute, get_connectivity_context_attribute, get_resource_name


class TestContextUtils(TestCase):
    def test_put_and_get_context(self):
        context = MagicMock()
        put_context(context)
        self.assertTrue(context == get_context())

    def test_put_context_raises_exception(self):
        context = None
        self.assertRaises(put_context, context)

    def test_get_attribute_by_name(self):
        attribute_name = 'test_attribute'
        attribute_value = 'value'
        context = ResourceCommandContext()
        context.resource = ResourceContextDetails()
        context.resource.attributes = {attribute_name: attribute_value}
        self.assertTrue(attribute_value == get_attribute_by_name(context=context, attribute_name=attribute_name))

    def test_get_resource_address(self):
        resource_address = 'address'
        context = ResourceCommandContext()
        context.resource = ResourceContextDetails()
        context.resource.address = resource_address
        self.assertTrue(resource_address == get_resource_address(context=context))

    def test_get_resource_name(self):
        resource_name = 'resource_name'
        context = ResourceCommandContext()
        context.resource = ResourceContextDetails()
        context.resource.name = resource_name
        self.assertTrue(resource_name == get_resource_name(context=context))

    def test_get_reservation_context_attribute(self):
        domain = 'domain_name'
        context = ResourceCommandContext()
        context.reservation = ReservationContextDetails()
        context.reservation.domain = domain
        self.assertTrue(domain == get_reservation_context_attribute('domain', context))

    def test_get_connectivity_context_attribute(self):
        server_address = 'server_address'
        context = ResourceCommandContext()
        context.connectivity = ConnectivityContext()
        context.connectivity.server_address = server_address
        self.assertTrue(server_address == get_connectivity_context_attribute('server_address', context))


