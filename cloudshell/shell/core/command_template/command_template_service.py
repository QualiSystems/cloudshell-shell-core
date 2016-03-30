import re
from cloudshell.shell.core.command_template.command_template_validator import CommandTemplateValidator

_TEMPLATE_DICT = {}

def add_commands(commands):
    _TEMPLATE_DICT.update(commands)

class CommandTemplateService:

    _command_templates = {}
    _error_list = []

    @staticmethod
    def send_commands_list(commands_list, send_command_func=None):
        if not send_command_func:
            raise Exception("Need send command function")
        output = ""
        for command in commands_list:
            output += send_command_func(command)
        return output

    @staticmethod
    def execute_command_map(command_map, send_command_func=None):
        """
        Configures interface ethernet
        :param kwargs: dictionary of parameters
        :return: success message
        :rtype: string
        """

        commands_list = CommandTemplateService.get_commands_list(command_map)
        output = CommandTemplateService.send_commands_list(commands_list, send_command_func)
        CommandTemplateService._check_output_for_errors(output)
        return output


    @staticmethod
    def get_commands_list(command_map):
        prepared_commands = []
        for command, value in command_map.items():
            if command in CommandTemplateService._command_templates:
                command_template = CommandTemplateService._command_templates[command]
                prepared_commands.append(CommandTemplateValidator.get_validate_list(command_template, value))
        return prepared_commands

    @staticmethod
    def rollback():
        CommandTemplateService.execute_command_map({'rollback': []})