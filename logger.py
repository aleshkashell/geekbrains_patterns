import json
import logging
import logging.handlers


class Log:
    def __init__(self, name, path=None, log_level=None):
        self.logger = logging.getLogger(name)
        self.path = path if path else f'logs/{name}.log'
        levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "error": logging.ERROR,
            "warning": logging.WARNING
        }
        if not log_level:
            with open('conf.json') as f:
                data = json.load(f)
            try:
                log_level = data['log_level']
            except KeyError:
                log_level = "debug"
        try:
            self.log_level = levels[log_level.lower()]
        except KeyError:
            self.log_level = logging.DEBUG
        self._init_console_handler()
        self._init_file_handler()
        self.logger.setLevel(self.log_level)

    def _init_console_handler(self):
        formatter = logging.Formatter("%(asctime)-25s %(name)-30s %(levelname)-10s %(message)s")
        console = logging.StreamHandler()
        console.setLevel(self.log_level)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def _init_file_handler(self):
        formatter = logging.Formatter("%(asctime)-25s %(name)-30s %(levelname)-10s %(message)s")
        fh = logging.handlers.TimedRotatingFileHandler(
            self.path, when='D', interval=1, backupCount=5, encoding='utf-8')
        fh.setLevel(self.log_level)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
