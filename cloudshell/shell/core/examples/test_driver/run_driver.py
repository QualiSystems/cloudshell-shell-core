import threading

from test_driver import TestDriver
from cloudshell.shell.core.examples.test_driver.drivercontext import ResourceCommandContext, ResourceContextDetails, \
    ReservationContextDetails
from cloudshell.cli.connection_manager import ConnectionManager
import time

class DriverCommandExecution(threading.Thread):
    def __init__(self, driver_instance, command_name, parameters_name_value_map):
        threading.Thread.__init__(self)

        self._parameters_name_value_map = parameters_name_value_map
        self._driver_instance = driver_instance
        self._command_name = command_name
        # self._cancellation_context = CancellationContext()

    def run(self):
        self._result = self._driver_instance.invoke_func(self._command_name,
                                                         self._parameters_name_value_map)

    def set_cancellation_context(self):
        # self._cancellation_context.is_cancelled = True
        pass

    def get_result(self):
        return self._result


class DriverWrapper:
    def __init__(self, obj):
        self.instance = obj

    def invoke_func(self, command_name, params):
        func = getattr(self.instance, command_name)

        return func(**params)


tt = TestDriver()

# dd = DriverWrapper(TestDriver())

# context = 'dsadsad'
# context = ReservationContextDetails()
context = ResourceCommandContext()
context.resource = ResourceContextDetails()
context.resource.name = 'dsada'
context.reservation = ReservationContextDetails()
context.reservation.reservation_id = 'test_id'
context.resource.attributes = {}
context.resource.attributes['username'] = 'yar'
context.resource.attributes['password'] = 'Blt0k0ubz'
context.resource.attributes['host'] = 'localhost'


# def print_result(list):
#     while len(list) > 0:
#         for obj in list:
#             if not obj.isAlive():
#                 print(obj.get_result())
#                 list.remove(obj)


# def print_pool_size():
#     for i in range(1,20):
#         cm = ConnectionManager()
#         print('Pool size: '+str(cm.get_pool_size()))
#         time.sleep(1)


class MyThread(threading.Thread):

    def __del__(self):
        print('Delete Thread: '+self.getName())


# threading.Thread(target=print_pool_size).start()

# def wait(tt):
#     time.sleep(tt)

# dd = threading.Thread(target=wait, args=[20])
MyThread(target=tt.simple_command, args=[context, '10']).start()
MyThread(target=tt.simple_command, args=[context, '10']).start()
MyThread(target=tt.simple_command, args=[context, '10']).start()

# threading.Thread(target=tt.simple_command, args=[context, '10']).start()
# threading.Thread(target=tt.simple_command, args=[context, '10']).start()
# threading.Thread(target=tt.simple_command, args=[context, '10']).start()
# dd = threading.Thread(target=tt.simple_command, args=[context, '10'])
# dd.start()

# while dd.is_alive:
#     pass



# print(tt.simple_command(context, '10'))
# tt.simple_command(context, '10')

# logger = get_context_based_logger(context)

# tt = DriverCommandExecution(dd, 'simple_command', {'context': context, 'command': '10'})
# tt.start()

# print(get_result(tt))


# dd = DriverCommandExecution(dd, 'simple_command', {'context': context, 'command': '10'})
# dd.start()
# print_result([tt, dd])
