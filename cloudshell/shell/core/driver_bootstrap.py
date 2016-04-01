import inject
import types
from cloudshell.shell.core.context.context_utils import get_context
from cloudshell.shell.core.dependency_injection.context_based_logger import get_logger_for_driver
from cloudshell.shell.core.handler_base import HandlerBase
from cloudshell.shell.core import driver_config


class DriverBootstrap(object):
    BASE_CONFIG = driver_config

    def __init__(self):
        self._config = None
        self.add_config(DriverBootstrap.BASE_CONFIG)

    def add_config(self, config):
        if not hasattr(self, '_config') or not self._config:
            self._config = types.ModuleType('config')
        if isinstance(config, types.ModuleType):
            for attr in filter(lambda x: x.isupper() and not x.startswith('__'), dir(config)):
                setattr(self._config, attr, getattr(config, attr))

    def _configure(self, binder):
        self.base_configuration(binder)
        self.configuration(binder)

    def initialize(self):
        if not inject.is_configured():
            inject.configure(self._configure)

    def base_configuration(self, binder):

        # Driver configuration
        binder.bind('config', self._config)

        # Binding for context
        binder.bind_to_provider('context', get_context)

        # Binding for logger
        binder.bind_to_provider('logger', get_logger_for_driver)

        # Binding from handler Class
        binder.bind('handler_class', HandlerBase)

        # Binding for API
        binder.bind('api', 'sdsd')


    def configuration(self, binder):
        pass