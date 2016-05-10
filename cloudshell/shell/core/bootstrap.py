from inject import Binder
from cloudshell.shell.core.context_utils import get_context
from cloudshell.core.logger import qs_logger


def configure(binder=Binder):

    # Binding for context
    binder.bind_to_provider('context', get_context)

    #Binding for loger
    binder.bind_to_provider('logger', qs_logger.get_qs_logger())

