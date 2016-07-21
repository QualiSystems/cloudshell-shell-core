import traceback

from cloudshell.core.context.context_service import ContextBasedService


class LoggingSessionContext(ContextBasedService):
    def __init__(self, context, logger):
        self.context = context
        self.logger = logger

    def get_objects(self):
        return self

    def context_started(self):
        return self

    def context_ended(self, exc_type, exc_value, exc_traceback):
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        self.logger.error('Error occurred: ' + ''.join(lines))
        return False
