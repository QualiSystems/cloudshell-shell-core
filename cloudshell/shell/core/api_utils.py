from cloudshell.shell.core.context_utils import get_attribute_by_name


def decrypt_password(api, password):
    """Uses api to decrypt password"""

    return api.DecryptPassword(password).Value


def decrypt_password_from_attribute(api, password_attribute_name, context=None):
    """Uses api to decrypt password"""

    password = get_attribute_by_name(password_attribute_name, context)
    return api.DecryptPassword(password).Value
