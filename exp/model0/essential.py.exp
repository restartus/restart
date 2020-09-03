"""Essential math.

Determine how to compress population into meaningful categories
"""
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def essential_name():
    """Set essential."""
    essential_name = ["Essential", "Non-essential"]
    return essential_name


def population_by_essentiality(model):
    """Set poulation by essential."""
    # Make it simple, just map healthcare to essential
    population_by_essentiality_array = np.eye(2)

    population_by_essentiality_df = pd.DataFrame(
        population_by_essentiality_array,
        index=model.essential_name,
        columns=model.population_label["name"],
    )

    return population_by_essentiality_df
