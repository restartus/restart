"""Utilities
"""
import logging


class Log:
    """Log helper class
    """

    def __init__(self, name):
        """helper function for logging
        """
        if name is None:
            name = "__main__"
        self.name = name
        self.log = logging.getLogger(name)
        # note this is for the logger, each stream has it's own level
        self.log.setLevel(logging.DEBUG)
        # this set console to get warnings from the commandline
        self.con = logging.StreamHandler()
        self.con.setLevel(logging.CRITICAL)
        self.con_format = logging.Formatter(
            "%(name)s - %(levelname)s - %(message)s"
        )
        self.con.setFormatter(self.con_format)
        # this is where you can bind as many handlers as you want
        self.log.addHandler(self.con)
        # create a file handler to dump stuff make sure to gitignore it
        # https://www.programcreek.com/python/example/472/logging.FileHandler
        self.fh = logging.FileHandler("test.log")
        self.fh.setLevel(logging.DEBUG)
        self.fh_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
        )
        self.fh.setFormatter(self.fh_format)
        self.log.addHandler(self.fh)
        self.mylog = self.class_log(self)
        self.mylog.debug(f"{self.mylog=}")

    def class_log(self, object):
        # breakpoint()
        class_log_name = self.name + "." + type(object).__name__
        self.log.debug(f"new logger {class_log_name=}")
        log = logging.getLogger(class_log_name)
        return log

    def module_log(self, name: str):
        module_log_name = self.name + "." + name
        log = logging.getLogger(module_log_name)
        return log

    def test_log(self, log):
        """Test all log messages emitted
        """
        log.debug("debug")
        log.warning("warning")
        log.error("error")
        log.critical("critical")
