class OrchestrationSavedArtifact:
    def __init__(self, artifact_type, identifier):
        """Represents a saved artifact according to the save and restore standard.

        This is a base class which can be extended with additional attributes
        required to later restore the artifact such as location or credentials.

        :param artifact_type: Describes the type of saved artifact
        (e.g. vCenter_image, tftp_file, network_location)
        :type artifact_type: str

        :param identifier: A unique identifier for the saved artifact
        (e.g the image url, a file full path)
        :type identifier: str
        """
        self.artifact_type = artifact_type
        self.identifier = identifier


class OrchestrationSaveResult:
    def __init__(self, saved_artifacts_info):
        """Container class for the orchestration_save result.

        :param saved_artifacts_info: An object describing the artifacts saved by
         this operation
        :type saved_artifacts_info: OrchestrationSavedArtifactInfo
        """
        self.saved_artifacts_info = saved_artifacts_info


class OrchestrationRestoreRules:
    def __init__(self, requires_same_resource, additional_rules=None):
        """Container class for the orchestration_save result.

        :type additional_rules: dict
        """
        if not additional_rules:
            additional_rules = {}
        self.requires_same_resource = requires_same_resource
        for rule in additional_rules:
            setattr(self, rule, additional_rules[rule])


class OrchestrationSavedArtifactInfo:
    def __init__(self, resource_name, created_date, restore_rules, saved_artifact):
        """This object describes the saved artifacts from a specific save operation.

        This information is stored and may later be sent to the Shell as a part of
        a restore operation.

        :param resource_name: The name of the resource on which the save operation
        was performed
        :type resource_name: str

        :param created_date: The time in which this save operation occurred
        :type created_date: datetime.datetime

        :param restore_rules: A list of rules governing constraints on restoring
        the saved artifact
        :type restore_rules: OrchestrationRestoreRules

        :param saved_artifact: The description of the saved artifact itself,
        the saved artifact can be of different types
        :type saved_artifact: OrchestrationSavedArtifact
        """
        self.resource_name = resource_name
        self.created_date = created_date.isoformat()
        self.restore_rules = restore_rules
        self.saved_artifact = saved_artifact
