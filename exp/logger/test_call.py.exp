"""Testing method calling.

Call testing
"""
import logging

# getting a method error


class Log:
    """Small Log class.

    Test log class
    """

    def __init__(self, name: str):
        """Init testing.

        Just get a logger
        """
        if name is None:
            name = __name__
        self.name = name
        self.log = logging.getLogger(name)

    def module_log(self, name):
        """Test module log.

        Basic scaffold
        """
        log_name = self.name + "." + name
        return logging.getLgger(log_name)


new_log = Log("test")

new_module_log = new_log.module_log(__name__)

new_log.log.debug(f"logging with {new_log.log=}")
