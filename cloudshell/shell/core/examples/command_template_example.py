from cloudshell.shell.core.command_template.command_template import CommandTemplate
from cloudshell.shell.core.command_template.command_template_service import CommandTemplateService

__author__ = 'shms'

def send_command(command):
    print command

TEST_TEMPLATE = {
    'configure_interface': CommandTemplate('interface {0}', r'[\w-]+\s*[0-9/]+',
                                           'Interface name is incorrect!')
}

CommandTemplateService.execute_command_map(TEST_TEMPLATE, send_command)