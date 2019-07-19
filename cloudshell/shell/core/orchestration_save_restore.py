import datetime

import jsonpickle

from cloudshell.shell.core.interfaces.save_restore import (
    OrchestrationRestoreRules,
    OrchestrationSavedArtifact,
    OrchestrationSavedArtifactInfo,
    OrchestrationSaveResult,
)


class OrchestrationSaveRestore(object):
    REQUIRED_SAVE_ATTRIBUTES_LIST = [
        "resource_name",
        ("saved_artifact", "identifier"),
        ("saved_artifact", "artifact_type"),
        ("restore_rules", "requires_same_resource"),
    ]

    def __init__(self, logger, resource_name):
        self._resource_name = resource_name
        self._logger = logger

    def prepare_orchestration_save_result(self, saved_file_path):
        artifact_type = saved_file_path.split(":")[0]
        identifier = saved_file_path.replace("{0}:".format(artifact_type), "")
        saved_artifact = OrchestrationSavedArtifact(
            identifier=identifier, artifact_type=artifact_type
        )
        saved_artifact_info = OrchestrationSavedArtifactInfo(
            resource_name=self._resource_name,
            created_date=datetime.datetime.now(),
            restore_rules=self._get_restore_rules(),
            saved_artifact=saved_artifact,
        )
        save_response = OrchestrationSaveResult(
            saved_artifacts_info=saved_artifact_info
        )
        self._validate_artifact_info_object(saved_artifact_info)

        return str(jsonpickle.encode(save_response, unpicklable=False))

    def parse_orchestration_save_result(self, saved_artifact_info, custom_params=None):
        if saved_artifact_info is None or saved_artifact_info == "":
            raise Exception(
                "ConfigurationOperations", "saved_artifact_info is None or empty"
            )

        saved_artifact = jsonpickle.decode(saved_artifact_info)
        saved_config = saved_artifact.get("saved_artifacts_info")
        if not saved_config:
            raise Exception(
                "ConfigurationOperations", "Saved_artifacts_info is missing"
            )
        params = {}
        if custom_params:
            params = jsonpickle.decode(custom_params)
            self._validate_custom_params(params)

        if (
            saved_config.get("restore_rules", {}).get("requires_same_resource")
            and saved_config.get("resource_name", "").lower()
            != self._resource_name.lower()
        ):
            raise Exception(
                "ConfigurationOperations",
                "Incompatible resource, expected {}".format(self._resource_name),
            )

        saved_artifact_dict = saved_config.get("saved_artifact", {})
        if not saved_artifact_dict:
            raise Exception()
        scheme = saved_artifact_dict.get("artifact_type")
        url_path = saved_artifact_dict.get("identifier")
        path = "{}:{}".format(scheme, url_path)
        restore_params = {
            "configuration_type": "running",
            "restore_method": "override",
            "vrf_management_name": None,
            "path": path,
        }

        custom_params_dict = params.get("custom_params")
        if custom_params_dict:
            restore_method = custom_params_dict.get("restore_method")
            if restore_method:
                restore_params["restore_method"] = restore_method

            configuration_type = custom_params_dict.get("configuration_type")
            if configuration_type:
                restore_params["configuration_type"] = configuration_type

            vrf_management_name = custom_params_dict.get("vrf_management_name")
            if vrf_management_name:
                restore_params["vrf_management_name"] = vrf_management_name

        if "startup" in url_path.split("/")[-1]:
            restore_params["configuration_type"] = "startup"
        return restore_params

    def _validate_artifact_info_object(self, saved_config):
        """Validate OrchestrationSavedArtifactInfo object for key components.

        :param OrchestrationSavedArtifactInfo saved_config: object to validate
        """
        is_fail = False
        fail_attribute = ""
        for class_attribute in self.REQUIRED_SAVE_ATTRIBUTES_LIST:
            if type(class_attribute) is tuple:
                if not hasattr(saved_config, class_attribute[0]):
                    is_fail = True
                    fail_attribute = class_attribute[0]
                elif not hasattr(
                    getattr(saved_config, class_attribute[0]), class_attribute[1]
                ):
                    is_fail = True
                    fail_attribute = class_attribute[1]
            else:
                if not hasattr(saved_config, class_attribute):
                    is_fail = True
                    fail_attribute = class_attribute

        if is_fail:
            raise Exception(
                "ConfigurationOperations",
                "Mandatory field {0} is missing in Saved Artifact Info "
                "request json".format(fail_attribute),
            )

    def _validate_custom_params(self, custom_params):
        if not custom_params.get("custom_params"):
            raise Exception(
                "ConfigurationOperations", "custom_params attribute is empty"
            )

    def _get_restore_rules(self):
        """Populate required restore rules.

        :return OrchestrationRestoreRules: response
        """
        self._logger.info("Creating Restore Rules")
        return OrchestrationRestoreRules(True)
