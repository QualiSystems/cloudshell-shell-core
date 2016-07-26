import types
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
def override_attributes_from_config(module, config=None):
    overridden_config = types.ModuleType('Overridden config')
    for attr in module.__dict__:
        if attr.isupper() and not attr.startswith('_'):
            if attr in config.__dict__:
                setattr(overridden_config, attr, config.__dict__[attr])
            else:
                setattr(overridden_config, attr, module.__dict__[attr])
    return overridden_config

