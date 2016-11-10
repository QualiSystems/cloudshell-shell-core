from cloudshell.shell.core.driver_context import AutoLoadResource, AutoLoadAttribute


class BaseResource(object):
    def __init__(self, resource_model='', name='', relative_address='', unique_id=None):
        self.resource_model = resource_model
        self.name = name
        self.relative_address = relative_address
        self.unique_id = unique_id
        self.attributes = {}

    def get_resource(self):
        if self.name:
            return AutoLoadResource(model=self.resource_model, name=self.name, relative_address=self.relative_address,
                                    unique_identifier=self.unique_id)

    def get_attributes(self):
        result = []
        for name, value in self.attributes.iteritems():
            result.append(AutoLoadAttribute(relative_address=self.relative_address, attribute_name=name,
                                            attribute_value=value))
        return result
