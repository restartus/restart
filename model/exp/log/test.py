"""Testing of logging function.

Test case
"""
import logging


def set_handler():
    """Create a handler.

    Duplicate
    """
    log = logging.getLogger("set_handler")
    # note this is for the logger, each stream has it's own level
    log.setLevel(logging.DEBUG)

    # this set console to get warnings from the commandline
    con = logging.StreamHandler()
    con.setLevel(logging.CRITICAL)
    con_format = logging.Formatter(
        "%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    )
    con.setFormatter(con_format)
    # this is where you can bind as many handlers as you want
    log.addHandler(con)

    # create a file handler to dump stuff make sure to gitignore it
    # https://www.programcreek.com/python/example/472/logging.FileHandler
    fh = logging.FileHandler("test.log")
    fh.setLevel(logging.DEBUG)
    fh_format = logging.Formatter(
        "%(asctime)s %(levelname)-8s "
        "[%(name)s:%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
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
