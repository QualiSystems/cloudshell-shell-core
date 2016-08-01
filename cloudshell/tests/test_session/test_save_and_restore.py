from unittest import TestCase
from cloudshell.shell.core.interfaces.OrchestrationSaveResult import OrchestrationSaveResult
from cloudshell.shell.core.interfaces.OrchestrationSavedArtifact import OrchestrationSavedArtifact
from cloudshell.shell.core.interfaces.OrchestrationSavedArtifactsInfo import OrchestrationSavedArtifactsInfo
import jsonpickle
from jsonschema import validate
import datetime


class TestSaveAndRestore(TestCase):

    def get_schema(self):
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "definitions": {
                "artifact": {
                    "type": "object",
                    "properties": {
                        "artifact_type": {
                            "type": "string"
                        },
                        "identifier": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "artifact_type",
                        "identifier"
                    ]
                }
            },
            "properties": {
                "saved_artifacts_info": {
                    "type": "object",
                    "properties": {
                        "resource_name": {
                            "type": "string"
                        },
                        "created_date": {
                            "type": "string",
                            "format": "date-time"
                        },
                        "restore_rules": {
                            "type": "object",
                            "properties": {
                                "requires_same_resource": {
                                    "type": "boolean"
                                }
                            },
                            "required": [
                                "requires_same_resource"
                            ]
                        },
                        "saved_artifact": {
                            "allOf": [
                                {
                                    "$ref": "#/definitions/artifact"
                                },
                                {
                                    "properties": {}
                                }
                            ],
                            "additionalProperties": True
                        }
                    },
                    "required": [
                        "resource_name",
                        "created_date",
                        "restore_rules",
                        "saved_artifact"
                    ]
                }
            },
            "required": [
                "saved_artifacts_info"
            ]
        }

    def test_serializes_to_schema(self):
        created_date = datetime.datetime.now()
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('test_type',identifier)

        saved_artifacts_info = OrchestrationSavedArtifactsInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules={'requires_same_resource': True},
            saved_artifact=orchestration_saved_artifact)

        orchestration_save_result = OrchestrationSaveResult(saved_artifacts_info)
        json_string = jsonpickle.encode(orchestration_save_result, unpicklable=False)
        validate(jsonpickle.loads(json_string), schema=self.get_schema())

