"""Utilities.

Main utilities
"""
import logging
from typing import Optional, Dict
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from pathlib import Path


def dump_loggers(logging, log: logging.Logger):
    """Dump all logs.

    Dump everything the logging system
    """
    log.critical(f"{logging.Logger.manager.loggerDict=}")
    for name in logging.Logger.manager.loggerDict.keys():
        lg = logging.getLogger(name)
        log.critical(f"{lg=}")
        log.critical(f"{lg.hasHandlers()=}")
        for h in lg.handlers:
            log.critical(f"{h=}")


def is_dir_or_file(name: str) -> bool:
    """Is path a directory or a file.

    It's hard to believe this is not a function already
    """
    path = Path(name)
    if path.is_dir() or path.is_file():
        return True
    return False


# sets the frame properly but does need to understand the model
# so goes into the model method
def set_dataframe(
    arr: np.ndarray, label: Dict, index: str = None, columns: str = None,
) -> pd.DataFrame:
    """Set the dataframe up.

    Using the model data Dictionary and labels
    """
    df = pd.DataFrame(arr, index=label[index], columns=label[columns],)
    df.index.name = index
    df.columns.name = columns
    return df


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

        if len(log.handlers) > 0:
            log.debug(f"{log=} already has {log.handlers=}")
            # breakpoint()
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
        self.log.debug(f"{self.log=}")
        # breakpoint()

    def log_class(self, object):
        """Class Logger.

        Creates a custom logger just for a class
        """
        class_log_name = self.name + "." + type(object).__name__
        self.log.critical(f"new logger {class_log_name=}")
        log = logging.getLogger(class_log_name)
        return log

    def log_module(self, name: str):
        """Create a logger for a module.

        Creates a logger specficaly for a file (a module in Python speak)
        """
        # breakpoint()
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
