import argparse
import os
import pandas as pd

from DatabaseManagement.utils import file_utils

def compare_output_files(path1: str, path2: str):
    df1, _ = file_utils.dataframe_from_file(path1)
    df2, _ = file_utils.dataframe_from_file(path2)

    assert all([df1.columns[i] == df2.columns[i] for i in range(len(df1.columns))])

    df1.sort_values(by=["Harness", "Signal_Net_Name"], inplace=True, ignore_index=True)
    df2.sort_values(by=["Harness", "Signal_Net_Name"], inplace=True, ignore_index=True)
    df1 = df1.astype(str)
    df2 = df2.astype(str)

    for x in df1.columns:
        df1[x] = df1[x].str.upper()
        df2[x] = df2[x].str.upper()

    pd.testing.assert_frame_equal(df1, df2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path1")
    parser.add_argument("--path2")
    args = parser.parse_args()
    compare_output_files(args.path1, args.path2)
