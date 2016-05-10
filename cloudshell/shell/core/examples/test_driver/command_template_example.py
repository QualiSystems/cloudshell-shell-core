from collections import OrderedDict

from cloudshell.shell.core.command_template.command_template import CommandTemplate
from cloudshell.shell.core.command_template.command_template_service import add_commands, execute_command_map

COMMIT_ROLLBACK = {'commit': CommandTemplate('commit', [], []),
                   'rollback': CommandTemplate('rollback', [], [])}
FIRMWARE_UPGRADE = {
    'firmware_upgrade': CommandTemplate('request system software add {0}', [r'.+'], ['Incorrect package path']),
    'reboot': CommandTemplate('request system reboot', [], [])}


class Handler:
    def __init__(self):
        add_commands(COMMIT_ROLLBACK)
        add_commands(FIRMWARE_UPGRADE)

    def send_command(self, command):
        print(command)

    def send(self, command):
        flow = OrderedDict()
        flow['firmware_upgrade'] = (command)

        execute_command_map(flow, self.send_command)


if __name__ == '__main__':
    tt = Handler()
    tt.send('dsdsds')
