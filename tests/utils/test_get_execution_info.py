from __future__ import annotations

from unittest.mock import Mock, patch

from cloudshell.shell.core.utils import get_execution_info


def test_execution_info_called_once():
    from cloudshell.shell.core.utils.execution_info import _exec_basic_info

    _exec_basic_info.clear()  # clear cache
    with patch("cloudshell.shell.core.utils.execution_info._get_shell") as sim:
        get_execution_info(Mock())
        get_execution_info(Mock())

        assert sim.call_count == 1
