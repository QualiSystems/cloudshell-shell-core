from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.core.context import ContextBasedService


class CloudShellSessionContext(ContextBasedService):
    def __init__(self, context):
        self.context = context

    def get_objects(self):
        return self.context_object

    @staticmethod
    def _get_domain(context):
        # noinspection PyBroadException
        try:
            return context.remote_reservation.domain
        except:
            return context.reservation.domain

    def context_started(self):
        self.context_object = CloudShellAPISession(host=self.context.connectivity.server_address,
                                                   token_id=self.context.connectivity.admin_auth_token,
                                                   username=None,
                                                   password=None,
                                                   domain=CloudShellSessionContext._get_domain(self.context))

        return self.context_object

    def context_ended(self, exc_type, exc_val, exc_tb):
        pass


class CloudShellContextFactory(object):
    def create(self, context):
        return CloudShellSessionContext(context)
