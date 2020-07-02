"""Utility functions
Some basic stuff that gets done over and over
"""
import logging


# https://stackoverflow.com/questions/40387735/why-does-not-logging-of-debug-level-output-anything
def setLogger(name: str, level=logging.WARNING):
    """Set logging parameters
    So they are just right and then set the logging level too
    """
    log = logging.getLogger(__name__)
    # just comment out the detail you want
    # log.setLevel(logging.WARNING)
    log.setLevel(level)
    stream = logging.StreamHandler()
    fmt = logging.Formatter("{filename}:{lineno} {message}", style="{")
    stream.setFormatter(fmt)
    log.addHandler(stream)
    return log
