import argparse
import os
import pandas as pd

def compare_output_files(path1: str, path2: str):
    file_ext1 = os.path.splitext(path1)[1]
    if file_ext1 == ".xlsx":
        df1 = pd.read_excel(path1, engine="openpyxl")
    elif file_ext1 == ".xls":
        df1 = pd.read_excel(path1, engine="xlrd")
    elif file_ext1 == ".csv":
        df1 = pd.read_csv(path1)
    else:
        raise Exception(f"We don't handle file type {file_ext1}")
    
    file_ext2 = os.path.splitext(path2)[1]
    if file_ext2 == ".xlsx":
        df2 = pd.read_excel(path2, engine="openpyxl")
    elif file_ext2 == ".xls":
        df2 = pd.read_excel(path2, engine="xlrd")
    elif file_ext2 == ".csv":
        df2 = pd.read_csv(path2)
    else:
        raise Exception(f"We don't handle file type {file_ext2}")

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
