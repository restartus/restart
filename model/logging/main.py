"""Testing of logging function
"""
import logging
from test_class import TestClass, test
from util import Log

log = logging.getLogger(__name__)
# note this is for the logger, each stream has it's own level
log.setLevel(logging.DEBUG)

# this set console to get warnings from the commandline
con = logging.StreamHandler()
con.setLevel(logging.CRITICAL)
con_format = logging.Formatter(
    "%(name)s - %(levelname)s - %(message)s"
)
con.setFormatter(con_format)
# this is where you can bind as many handlers as you want
log.addHandler(con)

# create a file handler to dump stuff make sure to gitignore it
# https://www.programcreek.com/python/example/472/logging.FileHandler
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
fh.setFormatter(fh_format)
log.addHandler(fh)

log.debug(f"debug for {__name__=}")
log.info(f"info for {__name__=}")
log.warning(f"warning for {__name__=}")
log.error(f"error for {__name__=}")
log.critical("critical")

# Now run this from the generic logger
# logging.warning(f"warning for {__name__=}")


def main():
    """Testing from main
    """
    new_log = Log('test')
    new_log.log.debug('first new_log entry')
    print("hello world")
    log.debug(f"{__name__=}")
    new_log.log.debug(f"{__name__=}")

    test(new_log)
    # note unlike Java, you cannot say test_class = TestClass
    # it thinks this is simple variable assignment
    test_class = TestClass(new_log)
    log.critical(f"found {test_class=}")
    new_log.log.critical(f"found {test_class=}")


if __name__ == "__main__":
    main()
