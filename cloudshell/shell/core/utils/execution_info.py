from __future__ import annotations

import platform
import socket
import threading
from contextlib import suppress

from cloudshell.rest.api import PackagingRestApiClient
from cloudshell.rest.exceptions import ShellNotFound
from cloudshell.rest.models import ShellInfo

from cloudshell.shell.core.context_utils import get_reservation_context_attribute
from cloudshell.shell.core.utils.get_installed_packages import get_installed_packages

_exec_basic_info = {}
_lock = threading.Lock()


def get_execution_info(context) -> dict[str, dict[str, str | tuple[str, ...]]]:
    """Aggregate information about execution server, reservation and shell."""
    info = _get_basic_info(context)

    with suppress(Exception):
        sandbox_info = {
            "Reservation ID": get_reservation_context_attribute(
                "reservation_id", context
            ),
            "Description": get_reservation_context_attribute("description", context),
            "Environment Name": get_reservation_context_attribute(
                "environment_name", context
            ),
            "Username": get_reservation_context_attribute("owner_user", context),
        }
        info["INFO"].update(sandbox_info)

    return info


def _get_basic_info(context) -> dict[str, dict[str, str | tuple[str, ...]]]:
    """Get info only once.

    This would be changed until the process is alive.
    """
    if _exec_basic_info:
        return _exec_basic_info.copy()

    with _lock:
        if not _exec_basic_info:
            info_level = {
                "Python Version": platform.python_version(),
                "Operating System": platform.platform(),
                "Platform": platform.system(),
                "Hostname": socket.gethostname(),
            }
            try:
                info_level["IP"] = socket.gethostbyname(info_level["Hostname"])
            except Exception:
                info_level["IP"] = "n/a"
            with suppress(Exception):
                info_level[
                    "CloudShell Version"
                ] = context.connectivity.cloudshell_version
            with suppress(Exception):
                shell = _get_shell(context)
                info_level["Shell Version"] = shell.version
                info_level["Shell Official"] = shell.is_official

            installed_packages = tuple(
                f"{name} == {version}"
                for name, version in sorted(get_installed_packages().items())
            )
            _exec_basic_info["INFO"] = info_level
            _exec_basic_info["DEBUG"] = {"Installed Packages": installed_packages}
    return _exec_basic_info.copy()


def _get_shell(context) -> ShellInfo:
    rest_api = PackagingRestApiClient(
        context.connectivity.server_address, context.connectivity.admin_auth_token
    )
    model = context.resource.model
    try:
        # get shell by model name
        shell = rest_api.get_shell_as_model(model)
    except ShellNotFound:
        # try to add "Shell" in the shell name
        if model.endswith(" 2G") and not model.endswith(" Shell 2G"):
            shell_name = model.replace(" 2G", " Shell 2G")
        else:
            raise
        shell = rest_api.get_shell_as_model(shell_name)

    return shell
