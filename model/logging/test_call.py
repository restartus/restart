"""Testing method clalling
"""
import logging
# getting a method error


class Log():
    def __init__(self, name: str):
        if name is None:
            name = __name__
        self.name = name
        self.log = logging.getLogger(name)

    def module_log(self, name):
        log_name = self.name + '.' + name
        return logging.getLgger(log_name)


new_log = Log('test')

new_module_log = new_log.module_log(__name__)

new_log.log.debug(f'logging with {new_log.log=}')
