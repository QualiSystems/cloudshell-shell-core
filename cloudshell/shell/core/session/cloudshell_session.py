from cloudshell.api.cloudshell_api import CloudShellAPISession


class CloudShellSessionContext(object):
    def __init__(self, context):
        """
        Initializes an instance of CloudShellSessionContext
        :param context: Command context
        :type: context: ResourceCommandContext
        """
        self.context = context

    @staticmethod
    def _get_domain(context):
        if hasattr(context, 'reservation') and context.reservation:
            return context.reservation.domain

        if hasattr(context, 'remote_reservation') and context.remote_reservation:
            return context.remote_reservation.domain

        return 'Global'

    def __enter__(self):
        """
        Called upon context start and initializes a session for CloudShell API
        :rtype: CloudShellAPISession
        :return :
        """
        self.context_object = CloudShellAPISession(host=self.context.connectivity.server_address,
                                                   token_id=self.context.connectivity.admin_auth_token,
                                                   username=None,
                                                   password=None,
                                                   domain=CloudShellSessionContext._get_domain(self.context))

        return self.context_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called upon end of the context. Does nothing
        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return:
        """
        pass
