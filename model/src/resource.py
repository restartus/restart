#
# Resource - Returns the names of all the resource in a list
#
# This contains
# This uses https://realpython.com/documenting-python-code/
# docstrings using the NumPy/SciPy syntax
# Uses a modified standard project
# Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
#

def resource_name():
    """Returns the name of all items that are resources

    Parameters
    ---------
    None

    Returns
    list[str]
        a list of all the resource names
    """
    return ('N95 Surgical', 'non-ASTM Mask')


class Resource:
    """The base class for all Resource in the model"""
    def __init__(self, name: str):
        self.name = name


class Resource_bharat(Resource):
    """Implements the simplest possible model with just two types"""
    """of resources"""
    pass
