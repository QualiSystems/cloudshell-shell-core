from json import JSONEncoder
from unittest import TestCase
import jsonpickle
from jsonschema import validate
import datetime
import json
from cloudshell.shell.core.interfaces.save_restore import OrchestrationSavedArtifact, \
    OrchestrationSavedArtifactInfo, OrchestrationSaveResult, OrchestrationRestoreRules


class SimpleJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return o.__dict__

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

        orchestration_saved_artifact = OrchestrationSavedArtifact('test_type', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
            saved_artifact=orchestration_saved_artifact)

        orchestration_save_result = OrchestrationSaveResult(saved_artifacts_info)
        json_string = jsonpickle.encode(orchestration_save_result, unpicklable=False)
        validate(jsonpickle.loads(json_string), schema=self.get_schema())

    def test_works_with_standard_json_serializer(self):
        created_date = datetime.datetime.now()
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('test_type', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
            saved_artifact=orchestration_saved_artifact)

        orchestration_save_result = OrchestrationSaveResult(saved_artifacts_info)

        result = json.dumps(orchestration_save_result, cls=SimpleJSONEncoder, indent=True)

        validate(json.loads(result), schema=self.get_schema())



    def test_can_serialize_custom_rules(self):
        created_date = datetime.datetime.now()
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('test_type', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True, additional_rules={'some_rule': 'True'}),
            saved_artifact=orchestration_saved_artifact)

        orchestration_save_result = OrchestrationSaveResult(saved_artifacts_info)
        json_string = jsonpickle.encode(orchestration_save_result, unpicklable=False)
        validate(jsonpickle.loads(json_string), schema=self.get_schema())

