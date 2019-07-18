import sys
from unittest import TestCase

import jsonpickle
from jsonschema import validate

from cloudshell.shell.core.orchestration_save_restore import OrchestrationSaveRestore

from tests.interfaces.test_save_and_restore import get_schema

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestOrchestrationSaveRestore(TestCase):
    def setUp(self):
        logger = MagicMock()
        resource_name = "Test"
        self._orch_obj = OrchestrationSaveRestore(
            logger=logger, resource_name=resource_name
        )

    def test_prepare_orchestration_save_result(self):
        file_path = "tftp://127.0.0.1/Test Folder/file.name"
        response = self._orch_obj.prepare_orchestration_save_result(file_path)
        validate(jsonpickle.loads(response), schema=get_schema())

    def test_parse_orch_save_result_no_custom_params(self):
        scheme = "tftp"
        folder_path = "//127.0.0.1/Test Folder/file.name"
        file_path = "{}:{}".format(scheme, folder_path)
        saved_artifact_info = self._orch_obj.prepare_orchestration_save_result(
            file_path
        )
        custom_params = None
        response = self._orch_obj.parse_orchestration_save_result(
            saved_artifact_info, custom_params
        )
        self.assertEqual(response.get("configuration_type"), "running")
        self.assertEqual(response.get("restore_method"), "override")
        self.assertEqual(response.get("path"), file_path)
        self.assertEqual(response.get("vrf_management_name"), None)

    def test_parse_orch_save_result_with_custom_params(self):
        custom_params = """
                {
                "custom_params": {
                        "vrf_management_name": "network-1"
                        }
                }"""
        scheme = "tftp"
        folder_path = "//127.0.0.1/Test Folder/file.name"
        file_path = "{}:{}".format(scheme, folder_path)
        saved_artifact_info = self._orch_obj.prepare_orchestration_save_result(
            file_path
        )
        response = self._orch_obj.parse_orchestration_save_result(
            saved_artifact_info, custom_params
        )
        self.assertEqual(response.get("configuration_type"), "running")
        self.assertEqual(response.get("restore_method"), "override")
        self.assertEqual(response.get("path"), file_path)
        self.assertEqual(response.get("vrf_management_name"), "network-1")
