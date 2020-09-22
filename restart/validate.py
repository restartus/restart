"""Short script for comparing two CSV files."""
import sys

import pandas as pd  # type: ignore

if __name__ == "__main__":

    # load in the dataframes
    try:
        df1 = pd.read_csv(sys.argv[1])
        df2 = pd.read_csv(sys.argv[2])
    except IndexError:
        print("usage: python validate.py <csv #1> <csv #2>")
        sys.exit()

    # sum all their rows
    sum1 = []
    for col in df1.columns:
        sum1.append(df1[col].sum())
    sum2 = []
    for col in df2.columns:
        sum2.append(df2[col].sum())

    # delete the first row that is just labels from both
    del sum1[0]
    del sum2[0]

    # calculate percent difference
    diff_list = []
    for i, val in enumerate(sum1):
        diff_list.append(float((sum2[i] - val) / val) * 100)

    # display output
    cols = list(df1.columns)[1:]

    print("------------------------")
    print("PERCENT DIFFERENCES")
    for i, val in enumerate(cols):
        print(f"{val}: {diff_list[i]}%")
    print("------------------------")
