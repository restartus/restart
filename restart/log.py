"""Log hierarchically.

Logging with a tree of loggers
"""
import logging
from pathlib import Path
from typing import Optional


def dump_loggers(logging, log: logging.Logger):
    """Dump all logs.

    Dump everything the logging system
    """
    log.debug(f"{logging.Logger.manager.loggerDict=}")
    for name in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(name)
        log.debug(f"{lg=}")
        log.debug(f"{lg.hasHandlers()=}")
        for h in lg.handlers:
            log.debug(f"{h=}")


class Log:
    """Log helper class.

    name: Name of logger
    parent: where to put the actual logging data

    To change logging levels at console:
        log_root.con.setLevel(logging.DEBUG)
        log_root.con.setLevel(logging.INFO)
    To change logging levels at file output
        log_root.fh.setLevel(logging.DEBUG)
        log_root.fh.setLevel(logging.INFO)

    Logging setting simplified
    """

    # https://stackoverflow.com/questions/39429526/how-to-specify-nullable-return-type-with-type-hints
    def __init__(self, name: Optional[str] = None, parent=None):
        """Initialize Log.

        Creates a logger and then sets output to file and output to console
        at different levels with the root name `name`.
        If no name passed, then use the name of the current directory.
        """
        if name is None:
            # https://stackoverflow.com/questions/3925096/how-to-get-only-the-last-part-of-a-path-in-python
            # https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
            # name = os.path.basename(os.getcwd())
            # https://realpython.com/python-pathlib/
            name = Path.cwd().name
        self.name = name
        # this is the main logging so at the top
        log = self.log = logging.getLogger(name)
        # the logger itself needs a level set as low as possible
        # otherwise the streams will not see it
        # https://docs.python.org/3/howto/logging-cookbook.html
        log.setLevel(logging.DEBUG)
        self.mylog = self.log_class(self)

        # streamlit can call multiple times and all variables are reset
        # except for logging. So here if the getLogger returns an
        # existing log, instead of creating new handlers, just look through the
        # existing ones and copy out the handlers. We use this for convenience
        # to set debugging levels by changing levels
        # like log_root.con.setLevel(logging.DEBUG)
        # or for all logs with log_root.log.setLevel(logging.WARNING)
        if len(log.handlers) > 0:
            log.warning(f"{log=} already has {log.handlers=}")
            # assume that the last streamhandler is for the console
            # the first handler is for the file logger
            for handler in log.handlers:
                if type(handler) is logging.StreamHandler:
                    self.con = handler
                    continue
                if type(handler) is logging.FileHandler:
                    self.fh = handler
                    continue
            return
        # note this is for the logger, each stream has it's own level
        # note that if name == __main__ you can set all logging too high
        #  self.log.setLevel(logging.DEBUG)
        # this set console to get warnings from the commandline
        self.con = logging.StreamHandler()
        self.con.setLevel(logging.CRITICAL)
        self.con_format = logging.Formatter(
            "%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
        )
        self.con.setFormatter(self.con_format)
        # this is where you can bind as many handlers as you want
        self.log.addHandler(self.con)
        # create a file handler to dump stuff make sure to gitignore it
        # https://www.programcreek.com/python/example/472/logging.FileHandler
        self.fh = logging.FileHandler(name + ".log")
        self.fh.setLevel(logging.DEBUG)
        # https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python
        # https://note.nkmk.me/en/python-long-string/
        self.fh_format = logging.Formatter(
            "%(asctime)s %(levelname)-8s "
            "[%(name)s:%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d:%H:%M:%S",
        )
        self.fh.setFormatter(self.fh_format)
        self.log.addHandler(self.fh)
        self.log.debug(f"{self.log=} f")
        # note we don't need self.fh, it is also accessible at
        # self.log.handlers[0] and self.log.handlers[1]

    def log_class(self, object):
        """Class Logger.

        Creates a custom logger just for a class
        """
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
        log.debug("test debug")
        log.warning("test warning")
        log.error("test error")
        log.critical("test critical")

        return self
