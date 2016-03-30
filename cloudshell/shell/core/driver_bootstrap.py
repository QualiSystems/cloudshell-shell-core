import inject
from cloudshell.shell.core.context.context_utils import get_context
from cloudshell.shell.core.dependency_injection.context_based_logger import get_logger_for_driver
from cloudshell.shell.core.handler_base import HandlerBase


class DriverBootstrap(object):
    def __init__(self):
        pass

    def _configure(self, binder):
        self.base_configuration(binder)
        self.configuration(binder)

    def initialize(self):
        if not inject.is_configured():
            inject.configure(self._configure)

    def base_configuration(self, binder):
        # Binding for context
        binder.bind_to_provider('context', get_context)

        # Binding for logger
        binder.bind_to_provider('logger', get_logger_for_driver)

        # Binding from handler Class
        binder.bind('handler_class', HandlerBase)

    def configuration(self, binder):
        pass