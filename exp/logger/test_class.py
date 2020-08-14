"""Test class for logging test.

Test scaffolding
"""
import logging

from log import Log


def test() -> Log:
    """Test log."""
    # the name of this is just at the root
    # it is not attached to main at all
    # this creates two loggers immediately
    # because of the dot notation

    log_name = "__main__." + __name__
    log = logging.getLogger(log_name)

    # for some reason when these are created
    # there is default formatting applied to the stdout
    # not clear from wherw

    print(f"print {__name__=}")
    log.critical(f"in {__name__=} with logger {log_name=}")

    # This will not sent anything because there are no handlers
    # if there it is below the level of handlers it is suppressed
    # the default handler is to stdout
    logging.debug(f"using generic logging debug now in {__name__=}")

    # Now run this from the generic logger
    logging.warning(f"warning for {__name__=}")
    root_log = Log("test")
    new_log = root_log.log_module(__name__)
    log.debug(f"{new_log=}")
    root_log.log.debug(f"logging with {root_log.log=}")
    return root_log


class TestClass:
    """Small Log class.

    Test log class
    """

    def __init__(self, root_log: Log):
        """Init testing.

        Just get a logger
        """
        self.root_log = root_log
        log = self.log = root_log.log_class(self)
        log.critical(f"made {log=} from {root_log=}")
        self.name = type(self).__name__
        self.mylog = logging.getLogger(self.name)

    def module_log(self, name):
        """Set Testing module log.

        Basic scaffold
        """
        log_name = self.name + "." + name
        return logging.get.Logger(log_name)
