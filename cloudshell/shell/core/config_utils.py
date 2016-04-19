import inject


@inject.params(config='config')
def get_config_attribute_or_none(attribute_name, config):
    attribute_value = None
    if hasattr(config, attribute_name):
        attribute_value = getattr(config, attribute_name)
    return attribute_value
