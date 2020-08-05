"""Test class for data."""
import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from data import Data

if __name__ == "__main__":
    """Run some tests for data class."""
    config = confuse.Configuration("config")
    arr = np.zeros((2, 1))
    desc = config["Description"]["Population p"]["Pop Detail pd"].get()
    ind = "Population p"
    cols = "Pop Detail d"
    data = Data(arr, desc, config=config, index=ind, columns=cols)

    print("-------ORIGINAL-------------")
    print("ARRAY")
    print(data.array)
    print("DF")
    print(data.df)
    print("ALT")
    print(data.alt)

    new_arr = np.ones((2, 1))

    print("--------CHANGE 1------------")
    data.array = new_arr
    print("ARRAY")
    print(data.array)
    print("DF")
    print(data.df)
    print("ALT")
    print(data.alt)

    data.df = pd.DataFrame([2, 2], index=["Hi", "There"], columns=["Yall"])

    print("--------CHANGE 2------------")
    print("ARRAY")
    print(data.array)
    print("DF")
    print(data.df)
    print("ALT")
    print(data.alt)
