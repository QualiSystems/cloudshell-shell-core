from weakref import WeakKeyDictionary
from threading import currentThread

from cloudshell.api.cloudshell_api import CloudShellAPISession

import inject

_API_CONTAINER = WeakKeyDictionary()


@inject.params(context='context')
def get_cloudshell_api(context):
    if not currentThread() in _API_CONTAINER:
        _API_CONTAINER[currentThread()] = _open_new_api_connection(context)
    return _API_CONTAINER[currentThread()]


def _open_new_api_connection(context):
    if hasattr(context, 'connectivity') \
            and context.connectivity \
            and context.connectivity.__class__.__name__ == 'ConnectivityContext':

        if hasattr(context, 'reservation') \
                and context.reservation \
                and hasattr(context.reservation, 'domain'):
            domain = context.reservation.domain
        else:
            domain = 'Global'

        server_address = context.connectivity.server_address
        api_port = context.connectivity.cloudshell_api_port
        token = context.connectivity.admin_auth_token
        api = CloudShellAPISession(server_address, port=api_port, token_id=token, domain=domain)
        return api
    else:
        raise Exception('Connectivity context has not defined')
