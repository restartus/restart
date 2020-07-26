"""Resource usage by protection level returned.

Resources calculated here
"""
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def level_name():
    """Set the protection levels."""
    level_name = ["WA0", "WA1", "WA2", "WA3", "WA4", "WA5", "WA6"]
    return level_name


def level_by_population(model):
    """Set levels by population."""
    level_by_population_array = np.zeros(
        [len(model.population_label), len(model.level_name)]
    )
    # https://docs.python.org/3/library/pdb.html
    print("level_by_population", len(model.population_label))
    print("level_by_population shape", level_by_population_array.shape)
    level_by_population_array[0, -1] = level_by_population_array[0, -2] = 0.5
    level_by_population_array[1, 1] = 1.0

    level_by_population_df = pd.DataFrame(
        level_by_population_array,
        index=model.population_label["name"],
        columns=model.level_name,
    )
    return level_by_population_df


# This is rows that are levels adn then usage of each resource  or l, n
# When population become n x d, then there will be a usage
# level for each do, so this become d x p x n
def usage_by_level(model):
    """Set usage by level."""
    usage_by_level_array = [
        [0, 0],
        [0, 1],
        [0, 2],
        [0.1, 3],
        [0.2, 4],
        [0.3, 6],
        [1.18, 0],
    ]
    usage_by_level_df = pd.DataFrame(
        usage_by_level_array,
        columns=model.resource_name,
        index=model.level_name,
    )
    return usage_by_level_df
