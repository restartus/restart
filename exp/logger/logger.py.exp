"""Testing of logging function.

Test case
"""
import logging
from test import set_handler

from test_class import TestClass, test
from log import Log, dump_loggers


def main():
    """Test from main.

    Test scaffold
    """
    # this is the base logger not use the Log class
    log = logging.getLogger(__name__)
    # note this is for the logger, each stream has it's own level
    log.setLevel(logging.DEBUG)
    # Now run this from the generic logger
    # logging.warning(f"warning for {__name__=}")
    log.debug(f"{__name__=}")
    log.info("hello world")
    log.critical("critical")

    # now use the Log class
    root_log = Log("test")
    root_log.log.info(f"first {root_log=}")
    dump_loggers(logging, log)
    print("hello world")
    log.critical(f"{__name__=}")
    root_log.log.critical(f"{__name__=}")
    test_class = TestClass(root_log)
    log.critical(f"found {test_class=}")
    root_log.log.critical(f"found {test_class=}")

    more_root = test()
    more_root.log.info(f"{more_root=}")
    # note unlike Java, you cannot say test_class = TestClass
    # it thinks this is simple variable assignment

    set_handler()


if __name__ == "__main__":
    main()
