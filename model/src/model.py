from typing import List, Dict
# https://www.w3schools.com/python/python_classes.asp


class Model:
    """ Main model for planning
    It sets the dimensionality of the problem and also the names of all the
    elements. Each subsystem will take the dimensions and names as inputs.

    They then will create the correct tables for use by the main computation
    This model has pointers to the major elements of the model.

    Attr:
    name: the friendly string name
    labels: This is what structures the entire model with a list of labels
            The defaults are what give us the simplified Bharat model

    These are the name dimensions of each, the length of each is set to
    parameters

    resources: n resources being modeled
    resource Attribute: r attributes for a resource
    population: p labels defines the populations
    population Details: d details about each population
    consumption Levels: l levels of resource consumption
    essentiality: maps population down to e tiersc
    supply: s stockpile units


    population: for each p population, give the d details on each [pxd=1] and
                and the level of use pxl
    consumption: for each p population, give consumption of n resources [pxn]
    essential: for each e summary levels, bucket p populations [exp]
    supply: for each p population, gives the
    """
    def __init__(self, name,
                 label: Dict[str, List[str]] =
                 {"Resource": ["N95", "ASTM3"],
                  "Attribute": ["Units", "Dimensions"],
                  "Population": ["Healthcare workers",
                                 "Non-heathcare employees"],
                  "Details": ["People"],
                  "Consumption":  ['WA0', 'WA1', 'WA2', 'WA3',
                                          'WA4', 'WA5', 'WA6'],
                  "Essentiality": ["Essential", "Non-essential"],
                  "Supply Units": ["Days"]
                  }):

        self.name = name
        self.labels = label
