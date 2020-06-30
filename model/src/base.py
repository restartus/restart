"""Base class for all model
This is used mainly to determine whether
we need to iterate over it in the dashboard
"""
from typing import Dict


class Base:
    '''Base for all model classes
    '''
    # https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python
    def __init__(self):
        self.description: Dict[str: str] = {}
