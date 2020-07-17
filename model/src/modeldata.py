"""Model Data Stucture.

The core data from a model. While the Model class contains all kinds of
execution, this is just the data so easy to pass around
and not run into import bugs
"""
# https://realpython.com/python-data-classes/
# We could also used a named tuple, but this can lead to bugs
from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelData:
    """Model raw data.

    Data separated from the running Model
    """

    label: Dict[str, str]
    value: Dict
    description: Dict
    datapaths: Dict
