"""Testing of logging function.

Test case
"""
# https://michaelgoerz.net/notes/use-of-the-logging-module-in-python.html
import logging

from testtiny import test_tiny
from log import dump_loggers

# https://stackoverflow.com/questions/53780735/what-is-the-type-hint-for-a-any-python-module
# this doesn't help much since we want all the parameters of loggin
# from types import ModuleType


def tiny():
    """Tiny testing.

    Small tests of logging
    """
    # https://stackoverflow.com/questions/44188270/no-handlers-could-be-found-for-logger
    # note that there is a root hanlder with a default to basicConfig
    # this adds a StreamHanlder to the root logger
    # if yuou call anything ahead of time, it calls basicConfig

    log = logging.getLogger(__name__)
    print("after util")
    dump_loggers(logging, log)
    # from test_class import TestClass, test
    print("after test_tiny")
    test_tiny()
    dump_loggers(logging, log)
    # from util import Log

    # note this is for the logger, each stream has it's own level
    log.setLevel(logging.DEBUG)
    log.critical(f"{logging.Logger.manager.loggerDict=}")

    # Now run this from the generic logger
    # logging.warning(f"warning for {__name__=}")
    log.debug(f"{__name__=}")

    log.critical(f"{logging.Logger.manager.loggerDict=}")
    log.setLevel(logging.INFO)
    log.critical("hello world")


if __name__ == "__main__":
    tiny()
