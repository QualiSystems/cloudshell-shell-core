from __future__ import annotations

import re
from importlib import metadata


def _normalize_name(name: str) -> str:
    """Normalize package/project name to a lowercase, dash-separated key.

    This matches the behavior consumers expect (e.g. 'cloudshell-logging').
    Replace underscores, dots and repeated separators with a single dash.
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def get_installed_packages() -> dict[str, str]:
    """Get a dictionary of installed packages and their versions.

    Uses the stdlib `importlib.metadata` (available in Python 3.8+).
    """
    packages: dict[str, str] = {}
    for dist in metadata.distributions():
        # Prefer the declared project name from metadata; fall back to the
        # distribution name if missing.
        meta_name = dist.metadata.get("Name") or dist.metadata.get("name")
        if not meta_name:
            # As a last resort use the distribution's builtin name attribute
            # or the directory name.
            try:
                meta_name = dist.name  # type: ignore[attr-defined]
            except Exception:
                meta_name = getattr(dist, "_path", None)
                if meta_name:
                    meta_name = str(meta_name).split("/")[-1]
                else:
                    continue

        key = _normalize_name(meta_name)
        packages[key] = dist.version

    return packages
