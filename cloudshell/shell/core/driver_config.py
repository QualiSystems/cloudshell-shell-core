from collections import OrderedDict

from cloudshell.cli.connection_manager import SessionCreator
from cloudshell.cli.ssh_session import SSHSession

### Session information
from cloudshell.shell.core.context.context_utils import get_attribute_wrapper

CONNECTION_MAP = OrderedDict()

ssh_session = SessionCreator(SSHSession)

ssh_session.kwargs = {'username': get_attribute_wrapper('username'), 'password': get_attribute_wrapper('password'),
                      'host': get_attribute_wrapper('host')}

CONNECTION_MAP['ssh'] = ssh_session
# CONNECTION_MAP['tcp'] = SessionHelper(TCPSession)
# CONNECTION_MAP['tcp'].kwargs
# CONNECTION_MAP['console'] = SessionHelper(ConsoleSession,
#                                                    ['console_server_ip', 'console_server_user',
#                                                     'console_server_password', 'console_port'])
# CONNECTION_MAP['telnet'] = SessionHelper(TelnetSession)
# CONNECTION_MAP['ssh'] = SessionHelper(SSHSession)

CONFIG_MODE_PROMPT = r'.*#\s*$'
ERROR_LIST = []
