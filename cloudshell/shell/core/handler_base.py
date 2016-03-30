__author__ = 'g8y3e'
import socket

from cloudshell.cli import expected_actions
from cloudshell.snmp.quali_snmp import QualiSnmp
from cloudshell.api.cloudshell_api import CloudShellAPISession


class HandlerBase:
    EXPECTED_MAP = {'Username: *$|Login: *$': expected_actions.send_username,
                    'closed by remote host': expected_actions.do_reconnect,
                    'continue connecting': expected_actions.send_yes,
                    'Got termination signal': expected_actions.wait_prompt_or_reconnect,
                    'Broken pipe': expected_actions.send_command,
                    '[Yy]es': expected_actions.send_yes,
                    'More': expected_actions.send_empty_string,
                    '[Pp]assword: *$': expected_actions.send_password
                    }

    def __init__(self, connection_manager, logger=None):
        self._connection_manager = connection_manager
        self._session = None
        self._logger = logger
        self._prompt = '.*[>#] *$'
        self._params_sep = ' '
        self._command_retries = 3
        self._expected_map = HandlerBase.EXPECTED_MAP
        # Todo refactor snmp handler
        self._snmp_handler = None
        self._cloud_shell_api = None

    @property
    def cloud_shell_api(self):
        if not self._cloud_shell_api:
            hostname = socket.gethostname()
            testshell_ip = socket.gethostbyname(hostname)
            testshell_user = self.reservation_dict['AdminUsername']
            testshell_password = self.reservation_dict['AdminPassword']
            testshell_domain = self.reservation_dict['Domain']
            self._cloud_shell_api = CloudShellAPISession(testshell_ip, testshell_user, testshell_password,
                                                         testshell_domain)
        return self._cloud_shell_api

    def _send_command(self, command, expected_str=None, expected_map=None, timeout=30, retry_count=10,
                     is_need_default_prompt=True):
        if expected_map is None:
            expected_map = self._expected_map

        if not expected_str:
            expected_str = self._prompt
        else:
            if is_need_default_prompt:
                expected_str = expected_str + '|' + self._prompt

        if not self._session:
            self.connect()

        out = ''
        for retry in range(self._command_retries):
            try:
                out = self._session.hardware_expect(command, expected_str, timeout, expected_map=expected_map,
                                        retry_count=retry_count)
                break
            except Exception as e:
                self._logger.error(e)
                if retry == self._command_retries - 1:
                    raise Exception('Can not send command')
                self.reconnect()
        return out

    def set_parameters(self, json_object):
        self.attributes_dict = json_object['resource']
        self.reservation_dict = json_object['reservation']
        pass

    def _default_actions(self):
        pass

    def connect(self):
        self._session = self._connection_manager.get_session(self._prompt)
        self._default_actions()

    def create_snmp_handler(self):
        """
        Creates snmp handler if it is not yet created
        :param json_object: parsed json, to create snmp handler if its None
        """
        ip = self.attributes_dict['ResourceAddress']
        user = self.attributes_dict['SNMP V3 User']
        password = self.attributes_dict['SNMP V3 Password']
        private_key = self.attributes_dict['SNMP V3 Private Key']
        community = self.attributes_dict['SNMP Read Community']
        version = self.attributes_dict['SNMP Version']
        v3_user = None
        if not self._snmp_handler:
            if '3' in version:
                if user != '' and password != '' and private_key != '':
                    v3_user = {'userName': user, 'authKey': password, 'privKey': private_key}
                else:
                    self._logger.error('User or password or private key parameter is empty')
            else:
                if community == '':
                    self._logger.error('Community parameter is empty')
            self._snmp_handler = QualiSnmp(ip=ip, v3_user=v3_user, community=community, logger=self._logger)
            self._logger.info('SNMP handler created')

    def disconnect(self):
        if self._session:
            return self._session.disconnect()

    def reconnect(self, retries_count=5, sleep_time=15):
        if self._session:
            self._session.reconnect(self._prompt, retries_count, sleep_time)

        self._default_actions()
        self._logger.info('Session reconnected successfully!')

    def _get_session_handler(self):
        return self._session

    def _get_logger(self):
        return self._logger

    def set_expected_map(self, expected_map):
        self._expected_map = expected_map
