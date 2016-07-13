from weakref import WeakKeyDictionary
from threading import currentThread

from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.shell.core.context_utils import get_reservation_context_attribute, get_connectivity_context_attribute

import inject

_API_CONTAINER = WeakKeyDictionary()


@inject.params(context='context')
def get_cloudshell_api(context):
    if not currentThread() in _API_CONTAINER:
        _API_CONTAINER[currentThread()] = _open_new_api_connection(context)
    return _API_CONTAINER[currentThread()]


def _open_new_api_connection(context):
    domain = get_reservation_context_attribute('domain', context)
    if not domain:
        domain = 'Global'

    server_address = get_connectivity_context_attribute('server_address', context)
    api_port = get_connectivity_context_attribute('cloudshell_api_port', context)
    token = get_connectivity_context_attribute('admin_auth_token', context)

    api = CloudShellAPISession(server_address, port=api_port, token_id=token, domain=domain)
    return api
