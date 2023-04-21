from __future__ import annotations

import pkg_resources


def get_installed_packages() -> dict[str, str]:
    """Get a dictionary of installed packages and their versions."""
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
