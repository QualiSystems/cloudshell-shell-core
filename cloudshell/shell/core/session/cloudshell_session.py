from cloudshell.api.cloudshell_api import CloudShellAPISession


class CloudShellSessionContext(object):
    DEFAULT_DOMAIN = "Global"
    DEFAULT_API_SCHEME = "http"

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

        return CloudShellSessionContext.DEFAULT_DOMAIN

    @staticmethod
    def _get_api_scheme(context):
        result = CloudShellSessionContext.DEFAULT_API_SCHEME
        if context.connectivity and hasattr(context.connectivity, 'cloudshell_api_scheme'):
            result = context.connectivity.cloudshell_api_scheme
        return result

    def __enter__(self):
        """
        Called upon context start and initializes a session for CloudShell API
        :rtype: CloudShellAPISession
        :return :
        """

        self.context_object = self.get_api()

        return self.context_object

    def get_api(self):
        cloudshell_api_scheme = CloudShellSessionContext._get_api_scheme(self.context)
        if "https" in cloudshell_api_scheme.lower():
            try:
                result = CloudShellAPISession(host=self.context.connectivity.server_address,
                                              token_id=self.context.connectivity.admin_auth_token,
                                              username=None,
                                              password=None,
                                              cloudshell_api_scheme=CloudShellSessionContext._get_api_scheme(
                                                  self.context),
                                              domain=CloudShellSessionContext._get_domain(self.context))
            except TypeError:
                raise Exception(self.__class__.__name__, "Current version of cloudshell api does not support https")
        else:
            result = CloudShellAPISession(host=self.context.connectivity.server_address,
                                          token_id=self.context.connectivity.admin_auth_token,
                                          username=None,
                                          password=None,
                                          domain=CloudShellSessionContext._get_domain(self.context))
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called upon end of the context. Does nothing
        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return:
        """
        pass
