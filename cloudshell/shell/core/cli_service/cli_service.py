import time

from cloudshell.shell.core.cli_service.cli_service_interface import CliServiceInterface
from cloudshell.shell.core.cli_service.cli_exceptions import CommandExecutionException
import re
import inject


class CliService(CliServiceInterface):
    def __init__(self):
        self._config = inject.instance('config')
        self._error_list = self._config.ERROR_LIST
        self._config_mode_prompt = self._config.CONFIG_MODE_PROMPT
        self._prompt = self._config.DEFAULT_PROMPT
        self._expected_map = self._config.EXPECTED_MAP
        self._error_map = self._config.ERROR_MAP
        self._command_retries = self._config.COMMAND_RETRIES

    def update_error_list(self, error_list):
        self._error_list += error_list

    @inject.params(logger='logger', session='session')
    def send_config_command(self, command, expected_str=None, expected_map=None, timeout=30, retry_count=10,
                            is_need_default_prompt=False, logger=None, session=None):
        """Send command into configuration mode, enter to config mode if needed

        :param command: command to send
        :param expected_str: expected output string (_prompt by default)
        :param timeout: command timeout
        :return: received output buffer
        """

        self._enter_configuration_mode(session)

        if expected_str is None:
            expected_str = self._prompt

        out = self._send_command(command, expected_str, expected_map=expected_map, retry_count=retry_count,
                                 is_need_default_prompt=is_need_default_prompt, timeout=timeout, session=session)
        logger.info(out)
        return out

    @inject.params(logger='logger', session='session')
    def send_command(self, command, expected_str=None, expected_map=None, timeout=30, retry_count=10,
                     is_need_default_prompt=True, logger=None, session=None):

        """Send command in base mode

        :param cmd: command to send
        :param expected_str: expected output string (_prompt by default)
        :param timeout: command timeout
        :return: received output buffer
        """
        self.exit_configuration_mode(session)
        try:
            out = self._send_command(command, expected_str, expected_map=expected_map, retry_count=retry_count,
                               is_need_default_prompt=is_need_default_prompt, timeout=timeout, session=session)
        except CommandExecutionException as e:
            self.rollback()
            logger.error(e)
            raise e
        return out

    @inject.params(logger='logger')
    def _send_command(self, command, expected_str=None, expected_map=None, timeout=30, retry_count=10,
                      is_need_default_prompt=True, logger=None, session=None):

        """Send command
        :param command: command to send
        :param expected_str: expected output string (_prompt by default)
        :param timeout: command timeout
        :return: received output buffer
        """

        if not expected_map:
            expected_map = self._expected_map

        if not expected_str:
            expected_str = self._prompt
        else:
            if is_need_default_prompt:
                expected_str = expected_str + '|' + self._prompt

        out = ''
        for retry in range(self._command_retries):
            try:
                out = session.hardware_expect(command, expected_str, expect_map=expected_map,
                                              error_map=self._error_map, retries_count=retry_count,
                                              timeout=timeout)
                break
            except Exception as e:
                logger.error(e)
                if retry == self._command_retries - 1:
                    raise Exception('Can not send command')
                session.reconnect(self._prompt)
        return out

    def send_command_list(self, commands_list, send_command_func=send_config_command):
        output = ""
        for command in commands_list:
            output += send_command_func(command)
        return output

    @inject.params(logger='logger')
    def exit_configuration_mode(self, session=None, logger=None):
        """Send 'enter' to SSH console to get prompt,
        if config prompt received , send 'exit' command, change _prompt to DEFAULT
        else: return
        :return: console output
        """

        out = None
        for retry in range(5):
            out = self._send_command(' ', session=session)
            if re.search(self._config_mode_prompt, out):
                self._send_command('exit', session=session)
            else:
                break

        return out

    @inject.params(logger='logger')
    def _enter_configuration_mode(self, session=None, logger=None):
        """Send 'enter' to SSH console to get prompt,
        if default prompt received , send 'configure terminal' command, change _prompt to CONFIG_MODE
        else: return

        :return: True if config mode entered, else - False
        """

        out = None
        for retry in range(3):
            out = self._send_command(' ', session=session)
            if not out:
                logger.error('Failed to get prompt, retrying ...')
                time.sleep(1)

            elif not re.search(self._config_mode_prompt, out):
                out = self._send_command('configure', self._config_mode_prompt, session=session)

            else:
                break

        if not out:
            return False
        # self._prompt = self.CONFIG_MODE_PROMPT
        return re.search(self._prompt, out)

    def rollback(self):
        pass
