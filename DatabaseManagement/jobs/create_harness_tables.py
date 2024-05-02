import psycopg2
import DatabaseManagement.utils.database_handler as dh
from DatabaseManagement.utils import file_utils
import pandas as pd
import yaml
from typing import Dict, List, Tuple
import os
import argparse

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

    errors = None
    data = {}
    for harness_file in harness_files:
        harness_file_path = os.path.join(dir_path, harness_file)
        df = file_utils.dataframe_from_file(harness_file_path)
        
        # fill NA values based on schema
        values = {x: schema[x]["fillna"] for x in schema.keys()}
        # lower case all column names
        df.columns = df.columns.str.lower().str.strip()
        # don't use keyword column names in tables
        df.rename({"from": "source", "to": "target"}, axis=1, inplace=True)
        df = df.astype(str)
        df.fillna(value=values, inplace=True)
        
        # apply upper() to all columns so that we don't have issues with case difference
        # evaluating to true when we diff columns in the database. ::sigh:: :(
        for col in df.columns:
            df[col] = df[col].str.upper()

        data_col_names = sorted([x for x in df.columns])
        table_col_names = sorted(list(schema.keys()))

        if data_col_names != table_col_names:
            error_msg = f"Data in {harness_file} has the incorrect schema."
            if errors is None:
                errors = []
            errors.append(error_msg)
        else:
            data_list = df.to_dict(orient="records")
            table_num = harness_file.split("-")[-1].split(file_ext)[0]
            table_name = f"h{table_num}"
            data[table_name] = data_list

    return errors, data


def main(dir_path: str, drop=False):
    """
        Main function that will create tables and ingest data into them. If
        we want to drop existing tables before adding them, then we can specify
        with an optional parameter.

        Params
        ------
            * dir_path: string representing the path to the directory containing
                the data to be used for constructing the harness tables
            * drop: Optional boolean param, default = False. If True, then
                we will drop all tables that we are trying to create if they exist
    """
    schema = yaml.safe_load(open("DatabaseManagement/harness_schema.yaml"))
    harness_schema = schema["harness"]["columns"]
    errors, harness_data = ingest_harness_table_data(dir_path, harness_schema)

    if errors is not None:
        for error in error:
            print(error)

    conn = dh.get_conn()
    for key in harness_data.keys():
        
        # we can determine if we want to drop tables before creating them.
        if drop is True:
            if dh.table_exists(conn, key):
                dh.drop_table(conn, key)

        # create tables if they do not exist
        cols = list(harness_data[key][0].keys())
        column_info = {col: harness_schema[col]["type"] for col in cols}
        dh.create_table(conn, key, column_info)

    for key in harness_data.keys():
        dh.insert_records(conn, key, harness_data[key])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=bool, default=False)
    parser.add_argument("--dir_path", type=str)
    args = parser.parse_args()
    main(dir_path=args.dir_path, drop=args.drop)
