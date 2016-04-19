from collections import OrderedDict

from cloudshell.shell.core.context.context_utils import build_suitable_context
from cloudshell.shell.core.context.context import AutoLoadCommandContext, ResourceCommandContext, \
    ResourceRemoteCommandContext


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


# Handler configuration

# """Function or classobj for snmp handler creation"""
# SNMP_HANDLER = ""
#
# """Function or classobj for handler creation"""
# HANDLER_CLASS = ""
#
#
# # Session configuration
# """Function or Classobj for session creation"""
# GET_SESSION = ""
#
# """Default prompt used in CLI service"""
# DEFAULT_PROMPT = r'.*[>$#]\s*$'
#
# """Default config mode prompt used in CLI service"""
# CONFIG_MODE_PROMPT = r'.*#\s*$'
#
# """Default expected map used in CLI service"""
# EXPECTED_MAP = OrderedDict()
# # # ERROR_MAP = OrderedDict({r'.*':'ErrorError'})
#
# """Default error map used in CLI service"""
# ERROR_MAP = OrderedDict()
#
# """Send command retries"""
# COMMAND_RETRIES = 10
