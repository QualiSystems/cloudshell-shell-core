import imp

import inject
import os
import types
from cloudshell.shell.core.context.context_utils import get_context
from cloudshell.shell.core.dependency_injection.context_based_logger import get_logger_for_driver
from cloudshell.shell.core.handler_base import HandlerBase
from cloudshell.shell.core import driver_config
from cloudshell.cli.connection_manager import ConnectionManager
from cloudshell.shell.core.cli_service.cli_service import CliService
import cloudshell.configuration as configuration_path


def search_files(search_path, pattern):
    if not isinstance(search_path, list):
        search_path = [search_path]
    found_files = []
    for path in search_path:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                if file == pattern:
                    found_files.append(full_path)
            else:
                found_files += search_files(full_path, pattern)
    return found_files


def import_module(path):
    module_dir, module_file = os.path.split(path)
    module_name, module_ext = os.path.splitext(module_file)
    f, pathname, desc = imp.find_module(module_name, [module_dir])
    module_obj = imp.load_module(module_name, f, pathname, desc)
    f.close()
    return module_obj


class DriverBootstrap(object):
    BASE_CONFIG = driver_config

    def __init__(self):
        self._modules_configuration_path = configuration_path.__path__
        self._configuration_file_name = 'configuration.py'
        self._config = None
        self._load_configuration_for_modules()
        self.add_config(DriverBootstrap.BASE_CONFIG)

    def _load_configuration_for_modules(self):
        for config_path in search_files(self._modules_configuration_path, self._configuration_file_name):
            module = import_module(config_path)
            self.add_config(module)

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

    def base_configuration(self, binder=inject.Binder()):

        # Driver configuration
        binder.bind('config', self._config)

        # Binding for context
        binder.bind_to_provider('context', get_context)

        # Binding for logger
        binder.bind_to_provider('logger', get_logger_for_driver)

        binder.bind_to_constructor('connection_manager', ConnectionManager)

        # Session
        binder.bind_to_provider('session', self._config.GET_SESSION_FUNCTION)

        # Binding from handler Class
        binder.bind('handler_class', HandlerBase)

        # Binding for API
        binder.bind('api', 'sdsd')

        # CLI service
        binder.bind_to_provider('cli_service', CliService)

    def configuration(self, binder):
        pass
