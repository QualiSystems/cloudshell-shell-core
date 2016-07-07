from threading import Event, Lock


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
