from cloudshell.shell.core.context.context_utils import context_from_args
from cloudshell.shell.core.driver_bootstrap import DriverBootstrap
from cloudshell.shell.core.cli_service.cli_service import CliService
import inject
import test_config as config


class TestDriver:
    def __init__(self):
        bootstrap = DriverBootstrap()
        bootstrap.add_config(config)
        bootstrap.initialize()
        # self.config = inject.instance('config')

    @context_from_args
    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        return 'Finished initializing'

    # Destroy the driver session, this function is called everytime a driver instance is destroyed
    # This is a good place to close any open sessions, finish writing to log files
    def cleanup(self):
        pass

    @context_from_args
    @inject.params(logger='logger', context='context', handler='handler')
    def simple_command(self, context, command, logger=None, handler=None):
        # ss = 'dsd'
        # for i in range(0, int(command)):
        #     logger.info('Resource: ' + context.resource.name)
        #     time.sleep(1)
        # return logger.log_path
        # out = cli.send_command('ls')
        # out = cli.send_command('df -h')
        print(handler.send_dd())
        logger.info('Command completed')
        return None
