__author__ = 'g8y3e'

import os
import platform
from cloudshell.cli.ssh_manager import SSHManager
from cloudshell.cli.telnet_manager import TelnetManager

from cloudshell.core.logger import qs_logger
from cloudshell.cli.file_manager import FileManager
from cloudshell.cli.console_manager import ConsoleManager

from cloudshell.cli.connection_manager import ConnectionManager
from cloudshell.api.cloudshell_api import CloudShellAPISession


class HandlerFactory:
    # Specific handlers are added in __init__.py of corresponding package
    handler_classes = {}

    session_handler_classes = {
        'SSH': SSHManager,
        'TELNET': TelnetManager,
        'FILE': FileManager,
        'CONSOLE': ConsoleManager
    }

    @staticmethod
    def get_execution_info(reservation_details, qs_logger, qs_server_address='localhost'):
        reservation_info = {}
        reservation_info['Python version'] = platform.python_version()
        reservation_info['Operating System'] = platform.platform()
        reservation_info['Platform'] = platform.system()
        reservation_info['Hostname'] = qs_server_address

        reservation_info['ReservationID'] = reservation_details['ReservationId']

        if not reservation_details['ReservationId'] == 'Autoload':
            testshell_user = reservation_details['AdminUsername']
            testshell_password = reservation_details['AdminPassword']
            testshell_domain = reservation_details['Domain']
            testshell = CloudShellAPISession(qs_server_address, testshell_user, testshell_password, testshell_domain)
            ret = testshell.GetReservationDetails(reservation_details['ReservationId'])
            reservation_descriptiono = ret.ReservationDescription
            reservation_info['EnviromentName']='None'

            if hasattr(reservation_descriptiono, 'Topologies'):
                topologies = ret.ReservationDescription.Topologies
                if len(topologies) > 0:
                    reservation_info['EnviromentName'] = ret.ReservationDescription.Topologies[0]
            reservation_info['Username'] = testshell_user

        return reservation_info

    @staticmethod
    def get_logger(driver_name, logger=None, logger_params={}, reservation_info={}):
        """ Create logger handler with provided parameters

        :param driver_name:
        :param logger_params:
        :param logger:
        :param reservation_info:
        :return:
        """
        if not 'ReservationId' in logger_params['reservation_details']:
            logger_params['reservation_details']['ReservationId'] = 'Autoload'

        ret_logger = logger if logger else qs_logger.get_qs_logger(driver_name, logger_params['handler_name'],
                                                                   logger_params['reservation_details']['ReservationId'])

        execution_info = HandlerFactory.get_execution_info(logger_params['reservation_details'], ret_logger,
                                                           logger_params['qs_server_address'])
        execution_info['ResourceName'] = logger_params['handler_name']
        qs_logger.log_execution_info(ret_logger, execution_info )

        return ret_logger

    @staticmethod
    def create_handler(handler_name, host, username='', password='', session_handler_name='ssh', port=None,
                      timeout=10, logger=None, **kwargs):
        """ Create resource handler with provided attributes, create nessesari logger, connection manager and snmp_handler for it

        :param handler_name:
        :param host:
        :param username:
        :param password:
        :param session_handler_name:
        :param port:
        :param timeout:
        :param logger:
        :param kwargs:
        :return:
        """
        if 'logger_params' in kwargs:
            logger_params = kwargs['logger_params']
        else:
            logger_params={}

        if 'reservation_detail' in kwargs:
            reservation_info = kwargs['reservation_detail']
        else:
            reservation_info = {}
        if not logger:
            logger = HandlerFactory.get_logger(handler_name, logger, logger_params, reservation_info)

        connection_manager = ConnectionManager(username=username, password=password, host=host, port=port,
                                               timeout=timeout, logger=logger, connection_type=session_handler_name,
                                               **kwargs)

        return HandlerFactory.handler_classes[handler_name.upper()](connection_manager, logger)


if __name__ == '__main__':
    pass

