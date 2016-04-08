from collections import OrderedDict

"""Function which get context by argument and handle it before binding, or None if we use original context
    Example:
    def func(context):
       ...
       return context
"""
# CONTEXT_WRAPPER = build_suitable_context
CONTEXT_WRAPPER = None

"""Function or classobj for handler creation"""
HANDLER_CLASS = None

"""Function or Classobj for session creation"""
GET_SESSION = None

"""Default prompt used in CLI service"""
DEFAULT_PROMPT = r'.*[>$#]\s*$'

"""Default config mode prompt used in CLI service"""
CONFIG_MODE_PROMPT = r'.*#\s*$'

"""Default expected map used in CLI service"""
EXPECTED_MAP = OrderedDict()
# # ERROR_MAP = OrderedDict({r'.*':'ErrorError'})

"""Default error map used in CLI service"""
ERROR_MAP = OrderedDict()

"""Send command retries"""
COMMAND_RETRIES = 10