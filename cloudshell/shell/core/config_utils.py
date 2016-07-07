import inject
from cloudshell.configuration.cloudshell_shell_core_binding_keys import CONFIG


@inject.params(config=CONFIG)
def get_config_attribute_or_none(attribute_name, config):
    attribute_value = None
    if hasattr(config, attribute_name):
        attribute_value = getattr(config, attribute_name)
    return attribute_value


def call_if_callable(attribute):
    if attribute and callable(attribute):
        result = attribute()
    else:
        result = attribute
    return result


@inject.params(config=CONFIG)
def override_attributes_from_config(instance, config=None):
    for attr in dir(instance):
        if attr.isupper() and not attr.startswith('_') and hasattr(config, attr):
            setattr(instance, attr, getattr(config, attr))
