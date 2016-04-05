from collections import OrderedDict

from cloudshell.cli.connection_manager import SessionCreator
from cloudshell.cli.ssh_session import SSHSession
from cloudshell.cli.connection_manager import ReturnToPoolProxy
from cloudshell.shell.core.context.context_utils import get_attribute_wrapper
import inject

CONNECTION_MAP = OrderedDict()

CONNECTION_TYPE_SSH = 'ssh'
CONNECTION_TYPE_TELNET = 'telnet'
CONNECTION_TYPE_AUTO = 'auto'


def get_logger(context, api):
    return inject.instance('logger')


ssh_session = SessionCreator(SSHSession)
ssh_session.proxy = ReturnToPoolProxy
ssh_session.kwargs = {'username': get_attribute_wrapper('username'), 'password': get_attribute_wrapper('password'),
                      'host': get_attribute_wrapper('host'), 'logger': get_logger}

CONNECTION_MAP[CONNECTION_TYPE_SSH] = ssh_session
# CONNECTION_MAP['tcp'] = SessionHelper(TCPSession)
# CONNECTION_MAP['tcp'].kwargs
# CONNECTION_MAP['console'] = SessionHelper(ConsoleSession,
#                                                    ['console_server_ip', 'console_server_user',
#                                                     'console_server_password', 'console_port'])
# CONNECTION_MAP['telnet'] = SessionHelper(TelnetSession)
# CONNECTION_MAP['ssh'] = SessionHelper(SSHSession)


DEFAULT_CONNECTION_TYPE = CONNECTION_TYPE_AUTO
# CONNECTION_TYPE = get_attribute_wrapper('Connection Type')
CONNECTION_TYPE = CONNECTION_TYPE_SSH

POOL_TIMEOUT = 60

DEFAULT_PROMPT = r'.*[>$#]\s*$'
# PROMPT = DEFAULT_PROMPT
CONFIG_MODE_PROMPT = r'.*#\s*$'
ERROR_LIST = []

EXPECTED_MAP = OrderedDict()
# ERROR_MAP = OrderedDict({r'.*':'ErrorError'})
ERROR_MAP = OrderedDict()

COMMAND_RETRIES = 10

SESSION_POOL_SIZE = 1
