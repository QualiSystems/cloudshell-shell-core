from functools import wraps
from threading import Event, Lock


class GlobalLock(object):
    _event = Event()
    _event.set()
    _lock = Lock()

    @staticmethod
    def lock(func):
        @wraps(func)
        def _wrap_func(*args, **kwargs):
            with GlobalLock._lock:
                GlobalLock._event.wait()
                try:
                    GlobalLock._event.clear()
                    return func(*args, **kwargs)
                finally:
                    GlobalLock._event.set()

        return _wrap_func
