import numpy as np
import pandas as pd


class Essential():
    """Converts population to essentiality for simplicity

    Essential math
    determine how to compress population into meaningful categories
    We assume that we have the p population but define the e
    We take each row of population and then say what percent
    goes into which essential bucket

    """
    def __init__(self, model):

        # Make it simple, just map healthcare to essential
        self.from_population_pe_array = np.eye(2)

        # dimensions check
        assert(self.from_population_pe_array == model.dim.p)

        self.from_population_pe_df = pd.DataFrame(
                self.from_population_pe_array,
                index=model.label["Consumption"],
                columns=model.label["Population"])
