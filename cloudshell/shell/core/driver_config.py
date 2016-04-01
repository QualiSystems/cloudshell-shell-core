from collections import OrderedDict

from cloudshell.cli.connection_manager import SessionCreator
from cloudshell.cli.ssh_session import SSHSession



### Session information
CONNECTION_MAP = OrderedDict()

ssh_session = SessionCreator(SSHSession)

def test(attribute):
    def get_username(context, api):
            return context.get(attribute)
    return get_username


ssh_session.kwargs = {'username': test('asasa'), 'password': lambda context, api: context.password,
                      'host': lambda context, api: context.host}

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
