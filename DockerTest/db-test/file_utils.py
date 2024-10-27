from typing import Any, Dict
import os
import pandas as pd
import yaml
from typing import List, Tuple

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
    
    return df, file_ext

def read_yaml(file_path: str) -> Dict[str, Any]:
    """
        Given an absolute path to a yaml file, open and return the corresponding
        dict returned from the read
    """
    try:
        ret_dict = yaml.safe_load(open(file_path))
    except FileNotFoundError:
        print(f"The file {file_path} was not found, returning None...")
        ret_dict = None

    return ret_dict


def get_config_base_path():
    return os.path.join(os.path.dirname(__file__), ".", "config")

def get_harness_schema_path():
    return os.path.join(get_config_base_path(), "harness_schema.yaml")

def get_output_columns_path():
    return os.path.join(get_config_base_path(), "output_columns.yaml")

def get_select_columns_path():
    return os.path.join(get_config_base_path(), "select_columns.yaml")

def get_source_tables_path():
    return os.path.join(get_config_base_path(), "source_tables.yaml")

def ingest_harness_table_data(
    dir_path: str,
    schema: Dict[str, str]
) -> Tuple[List[str], Dict[str, List[Dict[str, str]]]]:
    """
        walk the directory path, check schema of each harness table
        against the harness schema, if the schema is wrong, catch and add error to
        a list with the table name and error message.

        Return a dict, keyed by table name, with values a list of dicts, each dict
        representing a row of data, therefore keyed by column name with value the value
        of that column for that row.
    """
    if not os.path.isdir(dir_path):
        raise Exception(f"A directory path must be passed, but we got {dir_path}, which is not a directory")
    
    all_files = os.listdir(dir_path)
    harness_files = [x for x in all_files if "Enterprise Harness Wirelist-" in x and os.path.isdir(x) is False]

    errors = None
    data = {}
    for harness_file in harness_files:
        harness_file_path = os.path.join(dir_path, harness_file)
        df, file_ext = dataframe_from_file(harness_file_path)

        # fill NA values based on schema
        values = {x: schema[x]["fillna"] for x in schema.keys()}
        # lower case all column names
        df.columns = df.columns.str.lower().str.strip()
        df.fillna(value=values, inplace=True)
        df = df.astype(str)
        
        # apply upper() to all columns so that we don't have issues with case difference
        # evaluating to true when we diff columns in the database. ::sigh:: :(
        for col in df.columns:
            df[col] = df[col].str.upper()

        data_col_names = sorted([x for x in df.columns])
        table_col_names = sorted(list(schema.keys()))

        table_num = harness_file.split("-")[-1].split(file_ext)[0]
        table_name = f"h{table_num}"
        if data_col_names != table_col_names:
            if errors is None:
                errors = []
            errors.append(table_name)
        else:
            data_list = df.to_dict(orient="records")
            data[table_name] = data_list

    return errors, data

def convert_to_csv(in_dir_path: str, out_dir_path: str):
    """
        Convert all (excel) files in in_dir_path to csv, and write out to
        out_dir_path
    """
    for fname in os.listdir(in_dir_path):
        df, _ = dataframe_from_file(os.path.join(in_dir_path, fname))
        fstub = os.path.splitext(fname)[0]
        new_fname = f"{fstub}.csv"
        df.to_csv(os.path.join(out_dir_path, new_fname), index=False, sep=",")
