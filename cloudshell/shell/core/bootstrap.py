from inject import Binder
import inject
from cloudshell.shell.core.context_utils import get_context
from cloudshell.shell.core.context_based_logger import get_context_based_logger
from cloudshell.shell.core.handler_base import HandlerBase


def base_configuration(binder=Binder):

    # Binding for context
    binder.bind_to_provider('context', get_context)

    # Binding for logger
    binder.bind_to_provider('logger', get_context_based_logger)

    # Binding from handler Class
    binder.bind('handler_class', HandlerBase)

    # # Binding for session
    # binder.bind_to_provider('session', get_session)
    #
    #
    # binder.bind_to_provider('thread_session', get_thread_session)
