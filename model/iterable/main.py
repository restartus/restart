"""Test Iterable.

Overall testing of iteration
"""
import logging
from typing import List
log = logging.Logger(__name__)


class Base():
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
class Model0():
    """List Model."""

    store: List[Base] = [Base('a'), Base('b')]
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


class Model():
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

    def __iter__(self):
        """Set up the index."""
        self.index = 0
        return self

    def __next__(self):
        """Index only through Base Object."""
        while name, value in vars(self.mode)
        self.index += 1
        return vars(self.model)[self.index]


def main():
    """Run Main.

    here we go
    """
    m = Model()
    for b in m:
        print(b)


if __name__ == "__main__":
    main()
