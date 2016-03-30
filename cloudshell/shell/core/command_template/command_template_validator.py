__author__ = 'g8y3e'

import re


class CommandTemplateValidator:
    @staticmethod
    def get_validate_list(command_tamplate, properties_list):
        if not isinstance(properties_list, list):
            properties_list = [properties_list]
            
        validate_result = CommandTemplateValidator._validate(properties_list, command_tamplate.get_re_string_list())
        if validate_result[0]:
            return command_tamplate.get_command(*properties_list)
        else:
            raise Exception(command_tamplate.get_error_by_index(validate_result[1]))

    @staticmethod
    def _validate(properties_list, re_string_list):
        if len(properties_list) != len(re_string_list):
            return (False, -1)

        if len(properties_list) == 0:
            return (True, -1)

        for index in range(0, len(properties_list)):
            if hasattr(re_string_list[index], '__call__'):
                if not re_string_list[index](properties_list[index]):
                    return (False, index)
            elif re.match(re_string_list[index], properties_list[index]) == None:
                return (False, index)

        return (True, -1)