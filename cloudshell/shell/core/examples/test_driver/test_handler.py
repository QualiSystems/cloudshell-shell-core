import inject


class TestHandler:
    @inject.params(cli='cli_service')
    def send_dd(self, cli=None):
        out = cli.send_command('ls')
        return out
