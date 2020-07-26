"""Test Iterable.

Overall testing of iteration
"""
import logging
from typing import List

log = logging.Logger(__name__)


class Base:
    """Base class.

    Testing
    """

    name: str

    def __init__(self, name: str):
        """Initialize.

        Testing
        """
        self.name = name


# test Model with a list
class Model0:
    """List Model."""

    store: List[Base] = [Base("a"), Base("b")]
    index: int

    def __init__(self):
        """Init."""
        pass

    # I know how to iterate,
    def __iter__(self):
        """Iterate Model."""
        self.index = -1
        log.debug(f"{self.index=}")
        return self

    # because https://www.w3schools.com/python/python_iterators.asp
    # with __iter__ then __next__ is called over and over
    def __next__(self):
        """Generate to go through store."""
        self.index += 1
        print(f"{self.index=}")
        if self.index >= len(self.store):
            raise StopIteration
        return self.store[self.index]


class Model:
    """Model objects."""

    # Class variables are shared by all instances, so you really want these
    # so you want these to be per instance, you put them in init
    # https://docs.python.org/3/tutorial/classes.html

    def __init__(self):
        """NO need to init."""
        self.population: Base = Base("population")
        self.resource: Base = Base("resource")
        self.demand: Base = Base("demand")
        self.index: int = 0
        self.name: str = __name__

    def __iter__(self):
        """Set up the index."""
        # this works because after Python 3.6 dictionaries are ordered
        # so create a list of the right keys and index through them
        # so make an index of Base objects
        # use a list comprehension that you can index through
        # breakpoint()
        # we need items because this converts a dictionary into a list
        # where each item is a tuple that is (key, value)
        self.list = [k for k, v in vars(self).items() if isinstance(v, Base)]
        log.critical(f"__iter_: {self.list=}")
        self.index = 0
        return self

    def __next__(self):
        """Index only through Base Object."""
        # https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
        # returns a dictionary of the name and the value, so n=2 is returns as
        # {'n' : 2 }
        # breakpoint()
        if self.index >= len(self.list):
            raise StopIteration
        obj = vars(self)[self.list[self.index]]
        log.critical(f"__next__: {self.index=} {obj=}")
        self.index += 1
        return obj


def main():
    """Run Main.

    here we go
    """
    m = Model()
    for b in m:
        print(b)


if __name__ == "__main__":
    main()
