import threading
import time
from Queue import Queue
import inject
import threading

class Fet:
    def do(self, tt):
        # with _LOCK:
        print(tt)


class ReturnToPoolProxy:
    def __init__(self, instance):
        self._instance = instance

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def __del__(self):
        if CM_INSTANCE:
            CM_INSTANCE.put_to_queue(self)
            print('Put')


class CM(object):
    _CM_INSTANCE = threading.Lock()
    def __new__(cls, *args, **kwargs):
        with cls._SINGLETON_LOCK:
            if not _CM_INSTANCE:
                _CM_INSTANCE = object.__new__(cls, *args, **kwargs)
        return _CM_INSTANCE

        @classmethod
        def is_defined(cls):
            defined = False
            if cls._instance:
                defined = True
            return defined

    def __init__(self):
        self.queue = Queue()
        self.put_to_queue(ReturnToPoolProxy(Fet()))
        print('CM created')

    def put_to_queue(self, obj):
        self.queue.put(obj)

    def get_from_queue(self):
        return self.queue.get(True, 10)

CM_INSTANCE = CM()
# _SINGLETON_LOCK = threading.Lock()

# class Singleton(object):
#     # _instance = None
#
#     def __new__(cls, *args, **kwargs):
#
#         if not CM_INSTANCE:
#             with _SINGLETON_LOCK:
#                  CM_INSTANCE = object.__new__(cls, *args, **kwargs)
#         return cls._instance
#
#     @classmethod
#     def is_defined(cls):
#         defined = False
#         if cls._instance:
#             defined = True
#         return defined



# QUEUE = Queue(maxsize=1)
# _LOCK = threading.Lock()








def config(binder=inject.Binder()):
    binder.bind_to_provider('obj', CM_INSTANCE.get_from_queue)

@inject.params(obj='obj')
def obj_print(ss, obj=None):
    obj.do(ss)
    time.sleep(1)



inject.configure(config)


def yy():
    for i in range(1,10):
        # obj = inject.instance('obj')
        # obj.do(i)
        # ff.do(i)
        # time.sleep(1)
        # QUEUE.put(ff)
        obj_print(i)
        # time.sleep(1)


threading.Thread(target=yy).start()
threading.Thread(target=yy).start()
threading.Thread(target=yy).start()
threading.Thread(target=yy).start()

# time.sleep(2)
# QUEUE.put(ReturnToPoolProxy(Fet()))


# Fet().start()
# Fet().start()
# Fet().start()