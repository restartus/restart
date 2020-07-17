"""Supply module.

Because cost will differ by group set it higher
"""
# This will get replaced later
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def cost_per_resource_by_essentiality(model):
    """Costing by essential."""
    cost_per_resource_by_essentiality_array = np.array([[3, 0.5], [4.5, 0.75]])

    cost_per_resource_by_essentiality_df = pd.DataFrame(
        cost_per_resource_by_essentiality_array,
        index=model.essential_name,
        columns=model.resource_name,
    )

    return cost_per_resource_by_essentiality_df


# This is essential stockpile by essential so e x n
def stockpile_required_by_essentiality(model):
    """Calculate required by essentiality."""
    # place holder just 30 days for essential and then zero for the rest
    stockpile_required_by_essentiality_array = np.array([[30, 30], [0, 0]])
    stockpile_required_by_essentiality = pd.DataFrame(
        stockpile_required_by_essentiality_array,
        index=model.essential_name,
        columns=model.resource_name,
    )
    return stockpile_required_by_essentiality
