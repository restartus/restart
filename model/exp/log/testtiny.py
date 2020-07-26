"""Test class for logging test.

Test scaffolding
"""
import logging

# from util import Log


# the name of this is just at the root
# it is not attached to main at all
# note if __main__ does not exist, it will create it
def test_tiny():
    """Test two classes in one.

    Two creted with one stringh
    """
    print(f"{__name__=}")
    log_name = "__main__." + __name__
    print(f"print {__name__=}")
    log = logging.getLogger(log_name)
    log.critical(f"{logging.Logger.manager.loggerDict=}")

    log.debug(f"in {__name__=} with logger {log_name=}")

    # This will not sent anything because there are no handlers
    logging.debug(f"using generic logging debug now in {__name__=}")

    # Now run this from the generic logger
    logging.warning(f"warning for {__name__=}")
