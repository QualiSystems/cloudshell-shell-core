from cloudshell.cli.session_types import SessionTypes
from cloudshell.cli.ssh_session import SSHSession

SessionTypes.SSH.classobj = SSHSession

SESSIONS = [SessionTypes.SSH]

CONFIG_MODE_PROMPT = r'.*#\s*$'
ERROR_LIST = []
