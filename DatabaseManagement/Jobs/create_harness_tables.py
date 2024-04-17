import psycopg2
import DatabaseManagement.database_handler as dh
import pandas as pd
import yaml
from typing import Dict, Any, Union, List, Tuple
import os

def ingest_harness_table_data(
    dir_path: str, schema: Dict[str, str]
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
    harness_files = [x for x in all_files if "harness-" in x and os.path.isdir(x) is False]

    errors = []
    data = {}
    for harness_file in harness_files:
        harness_file_path = os.path.join(dir_path, harness_file)
        file_ext = os.path.splitext(harness_file_path)[-1]
        if file_ext == ".xlsx":
            df = pd.read_excel(harness_file_path, engine="openpyxl")
        elif file_ext == ".csv":
            df = pd.read_csv(harness_file_path)
        else:
            raise Exception(f"We do not handle file types {file_ext}")

        data_col_names = sorted([x.lower().strip() for x in df.columns])
        table_col_names = sorted(list(schema.keys()))

        if data_col_names != table_col_names:
            error_msg = f"Data in {harness_file} has the incorrect schema."
            errors.append(error_msg)
        else:
            data_list = df.to_dict(orient="records")
            table_num = harness_file.split("-")[-1].split(file_ext)[0]
            table_name = f"h{table_num}"
            data[table_name] = data_list

    return errors, data


if __name__ == "__main__":
    schema = yaml.safe_load(open("DatabaseManagement/harness_schema.yaml"))
    harness_schema = schema["harness"]["columns"]
    dir_path = "/home/johnwillis/Lasp-Docs/Harness/HRN Tests"
    errors, harness_data = ingest_harness_table_data(dir_path, harness_schema)

    
