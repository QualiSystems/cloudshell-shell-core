from threading import Event, Lock


class GlobalLock(object):
    _EVENT = Event()
    _EVENT.set()
    _LOCK = Lock()

    @staticmethod
    def lock(func):
        def _wrap_lock_func(*args, **kwargs):
            with GlobalLock._LOCK:
                GlobalLock._EVENT.wait()
                try:
                    GlobalLock._EVENT.clear()
                    result = func(*args, **kwargs)
                finally:
                    GlobalLock._EVENT.set()
            return result
        return _wrap_lock_func

    @staticmethod
    def member(func):
        def _wrap_member_func(*args, **kwargs):
            GlobalLock._EVENT.wait()
            result = func(*args, **kwargs)
            return result
        return _wrap_member_func