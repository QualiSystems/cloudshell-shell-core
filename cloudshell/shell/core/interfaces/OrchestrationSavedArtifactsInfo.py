from cloudshell.shell.core.interfaces.OrchestrationSavedArtifact import OrchestrationSavedArtifact
from datetime import datetime

class OrchestrationSavedArtifactsInfo(object):
    def __init__(self, resource_name, created_date, restore_rules, saved_artifact):
        """
        :type resource_name: str
        :type created_date: datetime
        :type restore_rules: dict
        :type saved_artifact: OrchestrationSavedArtifact
        """
        self.resource_name = resource_name
        self.created_date = created_date
        self.restore_rules = restore_rules
        self.saved_artifact = saved_artifact