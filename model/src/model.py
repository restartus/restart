#
# Base class for everything that is storing frame
#
from typelib import List
from frame import Frame



# https://www.w3schools.com/python/python_classes.asp
class Model:
    """ Main model for planning
    This model has pointers to the major elements of the model
    Attr:
    population: for each p population, give the d details on each [pxd=1] and
                and the level of use pxl
    consumption: for each p population, give consumption of n resources [pxn]
    essential: for each e summary levels, bucket p populations [exp]
    supply: for each p population, gives the
    """
    def __init__(self, name, population=[], resource=[],
                 consumption=[], essential=[],
                 supply=[]):
        # population has population rows details
        self.population = population
        # self.resource_name = resource_name
        self.resource = resource
        self.consumption = consumption
        self.essential = essential
        self.supply = supply
        self.name = name
