import imp

import re

import inject
import os
import types
from cloudshell.shell.core.context.context_utils import get_context
from cloudshell.shell.core.dependency_injection.context_based_logger import get_logger_for_driver
from cloudshell.shell.core import driver_config
from cloudshell.shell.core.cli_service.cli_service import CliService
from cloudshell.core.logger.qs_logger import get_qs_logger

try:
    import cloudshell.configuration as configuration_path
except:
    configuration_path = None

CONFIGURATION_PATH = './configuration'


def search_files(search_path, pattern):
    """Recursively search file by pattern in specific path"""
    if not isinstance(search_path, list):
        search_path = [search_path]
    found_files = []
    for path in search_path:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                if re.search(pattern, file):
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
        self._logger = get_qs_logger('Bootstrap', 'QS', 'Generic resource')
        self._logger.debug('Initializing project')
        self._modules_configuration_path = configuration_path.__path__ or CONFIGURATION_PATH
        self._configuration_file_name_pattern = r'configuration.py$'
        self._bindings_file_name_pattern = r'bindings.py$'
        self._bindings_func_name = 'bindings'
        self._config = None
        self.add_config(DriverBootstrap.BASE_CONFIG)
        self._load_configuration_for_modules()

    def _load_configuration_for_modules(self):
        for config_path in search_files(self._modules_configuration_path, self._configuration_file_name_pattern):
            self._logger.debug('Load configuration ' + config_path)
            module = import_module(config_path)
            self.add_config(module)

    def _load_bindings_for_modules(self, binder):
        for binding_file in search_files(self._modules_configuration_path, self._bindings_file_name_pattern):
            self._logger.debug('Load binding ' + binding_file)
            module = import_module(binding_file)
            for key in filter(lambda x: x == self._bindings_func_name, dir(module)):
                attr = getattr(module, key)
                if callable(attr):
                    attr(binder)

    def add_config(self, config):
        self._logger.debug('Load configuration ' + config.__name__)
        if not hasattr(self, '_config') or not self._config:
            self._config = types.ModuleType('config')
        if isinstance(config, types.ModuleType):
            for attr in filter(lambda x: x.isupper() and not x.startswith('__'), dir(config)):
                setattr(self._config, attr, getattr(config, attr))

    def _configure(self, binder):
        self.base_configuration(binder)
        self._load_bindings_for_modules(binder)
        self.configuration(binder)

    def initialize(self):
        self._logger.debug('Initialize bindings')
        if not inject.is_configured():
            inject.configure(self._configure)

    def base_configuration(self, binder):

        """Driver configuration"""
        binder.bind('config', self._config)

        """Binding for context"""
        binder.bind_to_provider('context', get_context)

        """Binding for logger"""
        binder.bind_to_provider('logger', get_logger_for_driver)

        """Binding for session"""
        binder.bind_to_provider('session', self._config.GET_SESSION)

        """Binding for API"""
        binder.bind('api', 'sdsd')

        """Binding for CLI service"""
        binder.bind_to_provider('cli_service', CliService)

        """Binding for snmp handler"""
        binder.bind_to_provider('snmp_handler', self._config.SNMP_HANDLER)

        """Binding for handler"""
        binder.bind_to_provider('handler', self._config.HANDLER_CLASS)


    def configuration(self, binder):
        pass
