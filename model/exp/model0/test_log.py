"""Debug logging.

# note you can't name this logging.py as this would mask the real logging
# https://stackoverflow.com/questions/53825041/attributeerror-module-logging-has-no-attribute-basicconfig?noredirect=1&lq=1
# https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
"""
import logging

# without the config this should not print
logging.basicConfig(level=logging.DEBUG)
logging.debug("in first")


def main():
    """Test logging."""
    # this does not work, but works if it is in the main code
    logging.basicConfig(level=logging.INFO)
    logging.debug("in main")


if __name__ == "__main__":
    # this does not print
    print("in main")
    logging.basicConfig(level=logging.INFO)
    logging.info("in __name__ info")
    main()
