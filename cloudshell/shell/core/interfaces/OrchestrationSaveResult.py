from cloudshell.shell.core.interfaces.OrchestrationSavedArtifactsInfo import OrchestrationSavedArtifactsInfo


class OrchestrationSaveResult(object):
    def __init__(self, saved_artifacts_info):
        """
        :type saved_artifacts_info: OrchestrationSavedArtifactsInfo
        """
        self.saved_artifacts_info = saved_artifacts_info
