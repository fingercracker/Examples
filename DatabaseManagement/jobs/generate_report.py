import DatabaseManagement.database_handler as dh
import pandas as pd
from typing import List
import os
import sys
import argparse

def main(input_tables: List[str], output_file: str):
    """
        given a list of input tables, trace all unique signals through
        the harnesses and output a report as a .xlsx file
    """
    conn = dh.get_conn()

    harness_tables = dh.select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={"table_schema": ("=", "public")}
    )

    harness_tables = [x["table_name"] for x in harness_tables]

    columns = ["Signal_Net_Name", "Harness", "Connector", "Connector_PIN", "Harness", "Connector", "Connector_PIN"]
    data_list = []

    for input_table in input_tables:
        print(f"processing input table {input_table}...")
        cols = [
            "harness",
            "mark",
            "wire",
            "net",
            "source",
            "target",
            "pin", 
            "pin_1"
        ]
        source_recs = dh.select_with_where(conn, input_table, cols=cols)

        target_names = [x["target"] for x in source_recs]
        source_names = [x["source"] for x in source_recs]
        source_only_recs = [x for x in source_recs if x["source"] not in target_names]

        tmp_data = []
        for rec in source_only_recs:
            signal_net_name = rec["net"]
            to_pin = rec["pin_1"]
            from_pin = rec["pin"]
            to_connector = rec["target"]
            from_connector = rec["source"]
            wire_type = rec["mark"]
            wire_description = rec["wire"]
            harness = rec["harness"]
            tmp_data = [signal_net_name, harness, from_connector, from_pin, harness, to_connector, to_pin]
            
            while harness is not None:
                # if the target harness shows up in the source column,
                # then do a self join
                if to_connector in source_names:
                    wheres = {
                        "net": ("=", signal_net_name),
                        "source": ("=", to_connector)
                    }
                else:
                    connector_split = to_connector.split("-")
                    if len(connector_split) == 3:
                        harness = connector_split[0].lower()
                    elif len(connector_split) == 4:
                        harness = "".join(connector_split[:2]).lower()
                    else:
                        harness = None

                    if harness not in harness_tables:
                        harness = None

                    wheres = {
                        "net": ("=", signal_net_name),
                        "pin": ("=", to_pin)
                    }

                if harness is not None:
                    recs = dh.select_with_where(
                        conn,
                        table_name=harness,
                        cols=cols,
                        wheres=wheres
                    )

                    num_recs = len(recs)
                    if num_recs == 1:
                        tmp_rec = recs[0]

                        harness = tmp_rec["harness"]
                        from_connector = tmp_rec["source"]
                        to_connector = tmp_rec["target"]
                        from_pin = tmp_rec["pin"]
                        to_pin = tmp_rec["pin_1"]

                        tmp_data += [harness, from_connector, from_pin, harness, to_connector, to_pin]
                    elif num_recs == 0: # dead end, empty data.
                        harness = None
                    elif num_recs > 1:
                        raise Exception(f"There should be at most one connecting harness but we got {num_recs}")

            tmp_data += [wire_type, wire_description]
            data_list.append(tmp_data)

    num_to_add = int((max([len(x) for x in data_list]) - 3)/6 - 1)
    columns += ["Harness", "Connector", "Connector_PIN", "Harness", "Connector", "Connector_PIN"] * num_to_add
    columns += ["Wire_Type", "Wire_Description"]

    # post process the data list. We need to potentially add blank columns to each row
    print("post processing...")
    num_cols = len(columns)
    counter = 0
    for row in data_list:
        row_len = len(row)
        if row_len < num_cols:
            tmp_row = row[:row_len-2] + [""]*(num_cols - row_len) + row[row_len-2:]
            data_list[counter] = tmp_row
        counter += 1

    df = pd.DataFrame(data_list, columns=columns)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_tables", nargs="+")
    parser.add_argument("--output_file", default="./test_output.csv")
    args = parser.parse_args()
    main(input_tables=args.input_tables, output_file=args.output_file)
