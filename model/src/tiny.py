"""Tiny Restart.us Main Module.

Minimal main.py called tiny.py to test interactions
"""

# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
# explains that you can split a class into separate files by
# putting these inside the class definition
# http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
# Before we move to full modules, just import locally
# https://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
import logging  # noqa:F401

# name collision https://docs.python.org/3/library/resource.html
# so can't use resource.py

# from config import Config


def tiny():
    """Test Logging.

    A stub
    """
    # This is the only way to get it to work needs to be in main
    # https://www.programcreek.com/python/example/192/logging.Formatter
    # the confit now seems to work
    # log = set_logger(__name__, level=logging.DEBUG)
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    # https://docs.python.org/3/howto/logging-cookbook.html
    log.debug(f"{__name__=}")
    log.info("hello world")
