class BaseVisibleException(Exception):
    """Exception that will be visible to the end user"""
    pass


class ShellException(BaseVisibleException):
    """Generic exception for hiding all internal ones"""
    pass
