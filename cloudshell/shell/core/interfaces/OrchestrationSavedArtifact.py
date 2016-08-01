class OrchestrationSavedArtifact(object):
    def __init__(self, artifact_type, identifier):
        """
        :type artifact_type: str
        :type identifier: str
        """
        self.artifact_type = artifact_type
        self.identifier = identifier
