"""Test class for data."""
import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from data import Data

if __name__ == "__main__":
    """Run some tests for data class."""
    # in the default config.yaml, thi is a (2,3) matrix
    shape = (2, 3)
    key = "population_pP_tr"
    config = confuse.Configuration("config")
    data = Data(key, config=config)

    print("-------ORIGINAL-------------")
    print("ARRAY")
    print(data.array)
    print("DF")
    print(data.df)
    print("NARROW")
    print(data.narrow)

    print("--------CHANGE 1------------")
    new_arr = np.ones((2, 3))
    data.array = new_arr
    print("ARRAY")
    print(data.array)
    print("DF")
    print(data.df)
    print("NARROW")
    print(data.narrow)

    print("--------CHANGE 2------------")
    data.df = pd.DataFrame(
        [[2, 3, 1], [1, 4, 5]],
        index=["Hi", "There"],
        columns=["Yall", "Test2", "Test3"],
    )
    print("ARRAY")
    print(data.array)
    print("DF")
    print(data.df)
    print("NARROW")
    print(data.narrow)
