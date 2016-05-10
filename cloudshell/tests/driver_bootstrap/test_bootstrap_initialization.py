from unittest import TestCase
import inject
from cloudshell.shell.core.driver_bootstrap import DriverBootstrap
import types


class TestBootstrapInitialization(TestCase):

    def setUp(self):
        inject.clear()

    def test_initialization(self):
        db = DriverBootstrap()
        db.initialize()
        self.assertTrue(inject.is_configured())

    def test_add_configuration(self):
        test_string = 'test attribute'
        test_module = types.ModuleType('test_config')
        test_module.TEST_ATTRIBUTE = test_string
        db = DriverBootstrap()
        db.add_config(test_module)
        db.initialize()
        self.assertTrue(inject.instance('config').TEST_ATTRIBUTE == test_string)
