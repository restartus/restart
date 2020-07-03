"""Test class for logging test
"""
import logging
from util import Log

# the name of this is just at the root
# it is not attached to main at all
log_name = '__main__.' + __name__
log = logging.getLogger(log_name)


# print(f'print {__name__=}')
log.debug(f'in {__name__=} with logger {log_name=}')


# This will not sent anything because there are no handlers
logging.debug(f'using generic logging debug now in {__name__=}')

# Now run this from the generic logger
# logging.warning(f"warning for {__name__=}")


def test(root_log: Log):
    new_log = root_log.module_log(__name__)
    new_log.debug(f'in {__name__=} with logger {log_name=}')
    print('print: test')
    log.debug('debug test()')
    new_log.debug('debug test()')
    # this defaults to console on warning
    log.warning('warning test()')
    new_log.warning('warning test()')


class TestClass:
    def __init__(self, root_log):
        if root_log is not None:
            self.new_log = root_log.class_log(TestClass)
        print(f'print TestClass {type(self).__name__=}')
        class_log = log_name + '.' + type(self).__name__
        log.debug(f'{class_log=}')
        self.new_log.debug(f'{class_log=}')
        self.log = logging.getLogger(class_log)
        self.log.warning(f'created {class_log=}')
        self.new_log.warning(f'created {class_log=}')
