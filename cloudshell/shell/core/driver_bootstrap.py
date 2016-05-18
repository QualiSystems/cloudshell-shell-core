import imp

import re
import inject
import os
import types
from cloudshell.shell.core import driver_config
from cloudshell.core.logger.qs_logger import get_qs_logger
from cloudshell.configuration.cloudshell_shell_core_binding_keys import CONFIG, LOGGER, API, CONTEXT

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
        self._config = types.ModuleType('config')
        self._bindings = []
        self.add_config(DriverBootstrap.BASE_CONFIG)
        # self._load_configuration_for_modules()

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
        if isinstance(config, types.ModuleType):
            for attr in filter(lambda x: x.isupper() and not x.startswith('__'), dir(config)):
                setattr(self._config, attr, getattr(config, attr))

    def add_bindings(self, bindings_func):
        self._bindings.append(bindings_func)

    def _configure(self, binder):
        for func in self._bindings:
            func(binder)
        self.base_bindings(binder)
        self.bindings(binder)
        self._load_bindings_for_modules(binder)

    def initialize(self):
        self._logger.debug('Initialize bindings')
        if not inject.is_configured():
            inject.configure(self._configure)

    def base_bindings(self, binder):
        """
        Base bindings
        :param binder: The Binder object for binding creation
        :type binder: inject.Binder

        """

        """Driver configuration"""
        binder.bind(CONFIG, self._config)

        """Binding for context"""
        try:
            binder.bind_to_provider(CONTEXT, self._config.GET_CONTEXT_FUNCTION)
        except inject.InjectorException:
            pass

        """Binding for logger"""
        try:
            binder.bind_to_provider(LOGGER, self._config.GET_LOGGER_FUNCTION)
        except inject.InjectorException:
            pass

        """Binding for API"""
        try:
            binder.bind_to_provider(API, self._config.GET_CLOUDSHELL_API_FUNCTION)
        except inject.InjectorException:
            pass

    def bindings(self, binder):
        """
        Bindings
        :param binder: The Binder object for binding creation
        :type binder: inject.Binder

        """
        pass
