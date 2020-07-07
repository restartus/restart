"""Utilities.

Main utilities
"""
import logging
import os
from typing import Optional


class Log:
    """Log helper class.

    Logging setting simplified
    """

    # https://stackoverflow.com/questions/39429526/how-to-specify-nullable-return-type-with-type-hints
    def __init__(self, name: Optional[str] = None):
        """Initialize Log.

        Creates a logger and then sets output to file and output to console
        at different levels with the root name `name`.
        If no name passed, then use the name of the current directory.
        """
        if name is None:
            # https://stackoverflow.com/questions/3925096/how-to-get-only-the-last-part-of-a-path-in-python
            # https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
            name = os.path.basename(os.getcwd())
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
        self.mylog = self.log_class(self)
        self.mylog.debug(f"{self.mylog=}")

    def log_class(self, object):
        """Class Logger.

        Creates a custom logger just for a class
        """
        # breakpoint()
        class_log_name = self.name + "." + type(object).__name__
        self.log.debug(f"new logger {class_log_name=}")
        log = logging.getLogger(class_log_name)
        return log

    def log_module(self, name: str):
        """Create a logger for a module.

        Creates a logger specficaly for a file (a module in Python speak)
        """
        module_log_name = self.name + "." + name
        log = logging.getLogger(module_log_name)
        return log

    def test(self, log):
        """Test all log messages emitted.

        Testing code run this to make sure all levels are used
        """
        log.debug("debug")
        log.warning("warning")
        log.error("error")
        log.critical("critical")
