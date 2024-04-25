import DatabaseManagement.database_handler as dh
import pandas as pd
from typing import List
import os
import sys
import argparse

def main(input_tables: List[str]):
    """
        given a list of input tables, trace all unique signals through
        the harnesses and output a report as a .xlsx file
    """
    conn = dh.get_conn()

    for input_table in input_tables:
        cols = [
            "harness",
            "mark",
            "wire",
            "net",
            "from",
            "to",
            "pin", 
            "pin_1"
        ]
        recs = dh.select_with_where(conn, input_table, cols=cols)
        df = pd.DataFrame.from_dict(recs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_tables", nargs="+")
    args = parser.parse_args()
    main(input_tables=args.input_tables)
