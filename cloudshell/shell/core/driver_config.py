from collections import OrderedDict

from cloudshell.cli.connection_manager import SessionCreator
from cloudshell.cli.ssh_session import SSHSession
from cloudshell.cli.connection_manager import ReturnToPoolProxy


### Session information
from cloudshell.shell.core.context.drivercontext import ResourceContextDetails

CONNECTION_MAP = OrderedDict()


def get_wrapper(attribute):
    def get_attribute(context, api):
        if not isinstance(context, ResourceContextDetails):
            raise Exception('Wrong context supplied')
        resolved_attribute = context.attributes.get(attribute)
        if not resolved_attribute:
            raise Exception('Attribute ' + attribute + ' is empty')
        return resolved_attribute
    return get_attribute

ssh_session = SessionCreator(SSHSession)
ssh_session.proxy = ReturnToPoolProxy
ssh_session.kwargs = {'username': get_wrapper('username'), 'password': get_wrapper('password'),
                      'host': get_wrapper('host')}

CONNECTION_MAP['ssh'] = ssh_session
# CONNECTION_MAP['tcp'] = SessionHelper(TCPSession)
# CONNECTION_MAP['tcp'].kwargs
# CONNECTION_MAP['console'] = SessionHelper(ConsoleSession,
#                                                    ['console_server_ip', 'console_server_user',
#                                                     'console_server_password', 'console_port'])
# CONNECTION_MAP['telnet'] = SessionHelper(TelnetSession)
# CONNECTION_MAP['ssh'] = SessionHelper(SSHSession)

CONNECTION_TYPE_AUTO = 'auto'
DEFAULT_CONNECTION_TYPE = CONNECTION_TYPE_AUTO
CONNECTION_TYPE = get_wrapper('Connection Type')


POOL_TIMEOUT = 60


DEFAULT_PROMPT = r'.*[>#]\s*$'

CONFIG_MODE_PROMPT = r'.*#\s*$'
ERROR_LIST = []
