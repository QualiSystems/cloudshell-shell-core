from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.core.context.context_service import ContextBasedService


class CloudShellSessionContext(ContextBasedService):
    def __init__(self, context):
        """
        Initializes an instance of CloudShellSessionContext
        :param context: Command context
        :type context: ResourceCommandContext
        """
        self.context = context
        self.context_object = None

    def get_objects(self):
        """
        Returns a session for interacting with CloudShell API
        :return: CloudShellAPISession
        :rtype CloudShellAPISession
        """
        return self.context_object

    @staticmethod
    def _get_domain(context):
        # noinspection PyBroadException
        try:
            return context.remote_reservation.domain
        except:
            return context.reservation.domain

    def context_started(self):
        """
        Called upon context start and initializes a session for CloudShell API
        :return:
        """
        self.context_object = CloudShellAPISession(host=self.context.connectivity.server_address,
                                                   token_id=self.context.connectivity.admin_auth_token,
                                                   username=None,
                                                   password=None,
                                                   domain=CloudShellSessionContext._get_domain(self.context))

        return self.context_object

    def context_ended(self, exc_type, exc_val, exc_tb):
        """
        Called upon end of the context. Does nothing
        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return:
        """
        pass