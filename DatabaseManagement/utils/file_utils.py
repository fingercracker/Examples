import os
import pandas as pd

def dataframe_from_file(path: str) -> pd.DataFrame:
    file_ext = os.path.splitext(path)[-1]
    if file_ext == ".xlsx":
        df = pd.read_excel(path, engine="openpyxl")
    elif file_ext == ".xls":
        df = pd.read_excel(path, engine="xlrd")
    elif file_ext == ".csv":
        df = pd.read_csv(path)
    elif "#" in file_ext:
        raise Exception(
            f"The file {path} appears to have a lock on it. Please close open input files and try again."
        )
    else:
        raise Exception(f"We do not handle file types {file_ext}")
    
    return df