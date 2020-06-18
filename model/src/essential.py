import numpy as np
import pandas as pd


class Essential():
    """Converts population to essentiality for simplicity

    Essential math
    determine how to compress population into meaningful categories
    We assume that we have the p population but define the e

    """
    def __init__(self, model):

        # Make it simple, just map healthcare to essential
        self.pop_essential_values = np.eye(2)

        self.pop_essentiality_df = pd.DataFrame(
                self.pop_essentiality_values,
                index=model.consume.labels,
                columns=model.population.pop_labels)
