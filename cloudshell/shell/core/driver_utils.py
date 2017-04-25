import collections
from threading import Event, Lock

from cloudshell.shell.core import exceptions


class GlobalLock(object):
    def __init__(self):
        self._event = Event()
        self._event.set()
        self._lock = Lock()

    @staticmethod
    def lock(func):
        def _wrap_lock_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrap_lock_func

    def _wrap_lock(self, func):
        def _wrap_func(*args, **kwargs):
            if func.__name__ == '_wrap_lock_func':
                with self._lock:
                    self._event.wait()
                    try:
                        self._event.clear()
                        result = func(*args, **kwargs)
                    finally:
                        self._event.set()
            else:
                self._event.wait()
                result = func(*args, **kwargs)
            return result

        return _wrap_func

    def __getattribute__(self, item):
        attr = super(GlobalLock, self).__getattribute__(item)
        if callable(attr) and not item.startswith('_'):
            return self._wrap_lock(attr)
        else:
            return attr


class ExceptionMappingContext(object):
    """Context class that will map/hide all internal Exception"""

    def __init__(self, logger, exception_map=None):
        """

        :param logging.Logger logger:
        :param dict exception_map:
        """
        self._logger = logger
        self._exception_map = collections.OrderedDict()

        if exception_map is not None:
            self._exception_map.update(exception_map)

        base_exception_map = {
            "cloudshell.cli.session_manager_impl.SessionManagerException": "Failed to get CLI Session"
        }

        for key, val in base_exception_map.iteritems():
            if key not in self._exception_map:
                self._exception_map[key] = val

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_value is None:
            return

        exc_type_str = ".".join([exc_type.__module__, exc_type.__name__])

        if exc_type in self._exception_map:
            msg = self._exception_map[exc_type]
            raise exceptions.ShellException(msg)

        elif exc_type_str in self._exception_map:
            msg = self._exception_map[exc_type_str]
            raise exceptions.ShellException(msg)

        elif isinstance(exc_value, exceptions.BaseVisibleException):
            raise

        else:
            # todo (A.Piddubny): raise some general exception and hide all unhandled exceptions
            # for now just re-raise exception
            # raise exceptions.ShellException("Sorry, something went wrong")
            raise
