from abc import ABCMeta
from abc import abstractmethod


class CliServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_command(self):
        pass

    @abstractmethod
    def send_config_command(self, cmd, expected_str=None, timeout=30):
        pass

    @abstractmethod
    def _enter_configuration_mode(self):
        pass

    @abstractmethod
    def _exit_configuration_mode(self):
        pass

    @abstractmethod
    def send_commands_list(self):
        pass
