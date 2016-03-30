from cloudshell.shell.core.cli_service.cli_service_interface import CliServiceInterface
from cloudshell.shell.core.command_template.command_template_service import CommandTemplateService
import re

class CliService(CliServiceInterface):

    def __init__(self):
        self._error_list = []

    def _check_output_for_errors(self, output):
        for error_pattern in self._error_list:
            if re.search(error_pattern, output):
                self.rollback()
                raise Exception(
                    'Output contains error with pattern: "{0}", for output: "{1}"'.format(error_pattern, output))
        return output

    def rollback(self):
        # CommandTemplateService.execute_command_map({'rollback': []})
        pass