"""
MOdel definition
https://www.w3schools.com/python/python_classes.asp
"""
from typing import List, Dict
import logging

LOG = logging.getLogger(__name__)
# https://reinout.vanrees.org/weblog/2015/06/05/logging-formatting.html
LOG.debug('in %s', __name__)


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
        resource Attribute: a attributes for a resource
        supply: s stockpile units
    population: p labels defines the populations
        population Details: d details about each population
        consumption Levels: l levels of resource consumption
        essentiality: maps population down to e tiersc

    """
    # https://satran.in/b/python--dangerous-default-value-as-argument
    # https://stackoverflow.com/questions/2…
    # do not do default assignment, it remembers it on eash call
    def __init__(self, name, label: Dict[str, List[str]] = None):
        if label is None:
            label = {"Resource": ["N95", "ASTM3"],
                     "Res Attribute": ["Units", "Dimensions"],
                     "Supply": ["Days"],
                     "Population": ["Healthcare workers",
                                    "Non-heathcare employees"],
                     "Pop Detail": ["People", "Runs"],
                     "Pop Consumption": ['WA0', 'WA1', 'WA2', 'WA3',
                                         'WA4', 'WA5', 'WA6'],
                     "Pop Level": ["Essential", "Non-essential"]
                     }

        self.name: str = name
        self.label: Dict[str, List[str]] = label

        # These are just as convenience functions for dimensions
        # and for type checking this is ugly should make it
        # for look for assign because we are just mapping label
        self.dim: Dict[str, int] = {'n': len(self.label['Resource']),
                                    'a': len(self.label['Res Attribute']),
                                    's': len(self.label['Res Supply']),
                                    'p': len(self.label['Population']),
                                    'd': len(self.label['Pop Detail']),
                                    'l': len(self.label['Pop Level']),
                                    'e': len(self.label['Pop Level'])
                                    }
