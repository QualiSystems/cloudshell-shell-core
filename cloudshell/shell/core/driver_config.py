from cloudshell.shell.core.context_utils import build_suitable_context, get_context
from cloudshell.shell.core.context import AutoLoadCommandContext, ResourceCommandContext, \
    ResourceRemoteCommandContext
from cloudshell.shell.core.dependency_injection.context_based_cloudshell_api import get_cloudshell_api
from cloudshell.shell.core.dependency_injection.context_based_logger import get_logger_for_driver


# Context configuration section

"""Function which get context by argument and handle it before binding, or None if we use original context
    Example:
    def func(context):
       ...
       return context
"""
CONTEXT_WRAPPER = build_suitable_context
# CONTEXT_WRAPPER = None

"""AutoLoadCommandContext type definition"""
AUTOLOAD_COMMAND_CONTEXT = AutoLoadCommandContext.__name__
"""ResourceCommandContext type definition"""
RESOURCE_COMMAND_CONTEXT = ResourceCommandContext.__name__
"""ResourceRemoteCommandContext type definition"""
RESOURCE_REMOTE_COMMAND_CONTEXT = ResourceRemoteCommandContext.__name__


# Default bindings configuration

"""Function used for default context binding"""
GET_CONTEXT_FUNCTION = get_context

"""Function used for default logger binding"""
GET_LOGGER_FUNCTION = get_logger_for_driver

"""Function used for default api binding"""
GET_CLOUDSHELL_API_FUNCTION = get_cloudshell_api
