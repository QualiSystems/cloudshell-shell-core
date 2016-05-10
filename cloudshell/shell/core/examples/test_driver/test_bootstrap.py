from cloudshell.shell.core.driver_bootstrap import DriverBootstrap


class TestBootstrap(DriverBootstrap):

    def configuration(self, binder):
        binder.bind_to_provider('handler', self._config.HANDLER_CLASS)
