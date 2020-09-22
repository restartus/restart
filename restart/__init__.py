"""Initialization script for restart package."""

# Version
__version__ = "2.6"

# Public interface for the model
from restart.data import Data  # type: ignore
from restart.restart import RestartModel  # type: ignore
