import database_handler as dh
from file_utils import read_yaml, get_select_columns_path, get_output_columns_path, get_source_tables_path
import pandas as pd
from typing import Dict, List, Tuple
import argparse
from datetime import datetime

def process_record(
        conn,
        rec: Dict[str, str],
        source_names: List[str],
        harness_tables: List[str], 
        cols: List[str]
    ) -> Tuple[List[str], List[str]]:
    """
        Process the record contained in the input dict rec. Trace the signal contained
        in that record through the harness tables until we reach the termination point
        for that signal.

        Params
        ------
            * conn: psycopg2 connection object for querying the database
            * rec: a dictionary keyed by column name representing a record returned from
                a query of the harness tables
            * source_names: the names of the harnesses that appear as sources
            * harness_tables: the comprehensive list of harness table names in the database
            * cols: columns that we wish to select when conducting a query

        Return
        ------
            * The path of the signal packed into a list containing the harness, source and target
                connectors, and source and target pins, along with the name of the signal
            * The list of errors detected for the record being processed
    """
    # grab the columns use for selection from the config
    select_cols_path = get_select_columns_path()
    select_cols = read_yaml(select_cols_path)

    # collect the respective records from the record
    harness_net_name = rec[select_cols["harness_net_name"]]
    to_pin = rec[select_cols["to_pin"]]
    from_pin = rec[select_cols["from_pin"]]
    to_connector = rec[select_cols["target"]]
    from_connector = rec[select_cols["source"]]
    from_harness = rec[select_cols["harness"]]
    wire_type = rec[select_cols["wire_type"]]

    # start building the data to be inserted into the report
    data_list = [[[to_connector, to_pin, from_connector, from_pin, from_harness, wire_type]]]

    errors = []

    while from_harness is not None:
        # if the target harness shows up in the source column,
        # then do a self join
        if to_connector in source_names:
            to_harness = from_harness
        else:
            connector_split = to_connector.split("-")
            if len(connector_split) == 3:
                to_harness = connector_split[0].lower()
            elif len(connector_split) == 4:
                to_harness = "".join(connector_split[:2]).lower()
            else:
                to_harness = None

        wheres = {
            select_cols["harness_net_name"]: ("=", harness_net_name),
        }

        if to_harness is not None:
            if to_harness.lower() not in harness_tables:
                to_harness = None

        if to_harness is not None:
            recs = dh.select_with_where(
                conn,
                table_name=to_harness,
                cols=cols,
                wheres=wheres
            )

            source_names = list(set([x[select_cols["source"]] for x in recs]))

            num_recs = len(recs)
            if num_recs > 0:
                tmp_recs, errs = validate_record(
                    recs=recs,
                    to_pin=to_pin,
                    to_connector=to_connector,
                    harness_net_name=harness_net_name,
                    from_harness=from_harness,
                    to_harness=to_harness,
                    wire_type=wire_type,
                    select_cols=select_cols
                )

                if errs is not None:
                    errors += errs

                if tmp_recs is None:
                    to_harness = None
                else:
                    tmp_data_list = []
                    for tmp_rec in tmp_recs:
                        to_harness = tmp_rec[select_cols["harness"]]
                        from_connector = tmp_rec[select_cols["source"]]
                        to_connector = tmp_rec[select_cols["target"]]
                        from_pin = tmp_rec[select_cols["from_pin"]]
                        to_pin = tmp_rec[select_cols["to_pin"]]
                        wire_type = tmp_rec[select_cols["wire_type"]]
                        
                        tmp_data_list.append([to_connector, to_pin, from_connector, from_pin, to_harness, wire_type])

                    data_list.append(tmp_data_list)
                    # data_list.append([to_connector, to_pin, from_connector, from_pin, to_harness, wire_type])

            else: # dead end, empty data.
                errors.append(f"There is no signal {harness_net_name} in harness table {to_harness}")
                to_harness = None

        # the target harness now becomes the source        
        from_harness = to_harness

    # report signal trace in reverse harness -> cdh; unpack the data into a single array corresponding
    # to a single row entry in the report
    tmp_rows = build_rows(data_list)

    rows = []
    for tmp_row in tmp_rows:
        # tmp_row.reverse()
        row = [harness_net_name] + tmp_row
        rows.append(row)
    return rows, errors

def build_rows(data_list: List[List[List[str]]]) -> List[List[str]]:
    """
        The input triply nested lists represents a tensor of arbitrary dimension, that
        we "recursively" flatten into a matrix, representing a tuple of rows.

        Params
        ------
            * data_list: a list of lists of lists of strings, representing a tensor of arbitrary
                dimension, which is then recursively flattened into a matrix (2d tensor). This is
                representing all possible paths of the signal across the harnesses
        
        Return
        ------
            * rows: a list of list of strings, each list of strings representing a row in a matrix, these
                rows being the distinct paths of each signal
    """
    rows = None
    for i in range(len(data_list)):
        tmp_rows = []
        for lst in data_list[i]:
            # lst.reverse()
            if rows is None:
                rows = []
                tmp_rows = [lst]
            else:
                for row in rows:
                    # tmp_rows.insert(0, row + lst)
                    tmp_rows.append(lst + row)

        rows = tmp_rows

    return rows

def validate_record(
    recs: List[Dict[str, str]],
    to_pin: str,
    to_connector: str,
    harness_net_name: str,
    from_harness: str,
    to_harness: str,
    wire_type: str,
    select_cols: Dict[str, str],
) -> Tuple[List[List[str]], List[str]]:
    """
        Given a collection of records resulting from a harness table query, check
        that the record is valid. If it is not, return a list of the errors that
        invalidate the record(s).

        Params
        ------
            * recs: a list of dicts keyed by column name with values the value of that row for that column
            * to_pin: pin to which signal is being mapped
            * to_connector: the connector to which the signal is going
            * harness_net_name: signal name per harness team spec
            * from_harness: the harness from which the signal is eminating
            * to_harness: the harness to which the signal is going
            * wire_type: this is actually the cable type that is carrying the given signal
            * select_cols: the columns from the database that we wish to select

        Return
        ------
            * ret_recs: a list of lists of strings, the strings being the values corresponding to select_cols
                for valid records given the signal of interest
            * errors: a list of strings, representing possible errors found within the validated records
                for the given signal of interest
    """
    errors = []
    ret_recs = None
    # body ground signal
    if harness_net_name == "SHIELD":
        for rec in recs:
            if rec[select_cols["harness_net_name"]] == harness_net_name and rec[select_cols["wire_type"]] == wire_type:
                return [rec], errors
        errors += [f"There is no {harness_net_name} signal in {to_harness} with wire type {wire_type}"]
    # signal going through a connector to a different harness
    elif to_harness != from_harness:
        for rec in recs:
            if rec[select_cols["from_pin"]] == to_pin:
                if ret_recs is None:
                    ret_recs = []
                ret_recs.append(rec)
            
            if rec[select_cols["wire_type"]] != wire_type:
                errors.append(f"Wire type mismatch in harness {to_harness} for signal {harness_net_name}")
        
        if ret_recs is None:
            pin_count = 0
        else:
            pin_count = len(ret_recs)
        if pin_count > 1:
            errors.append(f"Signal {harness_net_name} is assigned to {pin_count} pins on harness {to_harness}")
        elif pin_count == 0:
            errors.append(f"Signal {harness_net_name} is not assigned to pin {to_pin} on harness {to_harness}")
    # signal is going through a splice, an arm plug, or test plug
    elif to_harness == from_harness:
        if len(recs) > 0:
            for rec in recs:
                if rec[select_cols["source"]] == to_connector and rec[select_cols["harness_net_name"]] == harness_net_name:
                    if ret_recs is None:
                        ret_recs = []
                    ret_recs.append(rec)

            if ret_recs is None:
                rec_count = 0
            else:
                rec_count = len(ret_recs)
            if rec_count == 0:
                errors.append(
                    f"Signal {harness_net_name} terminates prematurely in harness {to_harness}"
                )
            if rec_count > 1:
                if to_connector[:2].lower() != "sp":
                    errors.append(
                        f"Signal {harness_net_name} appears multiple times in {from_harness} from connector {to_connector}"
                    )
        else:
            errors.append(f"Signal {harness_net_name} does not appear in {from_harness} at all.")
    else:
        errors.append(f"We have a scenario not yet covered in record validation for {harness_net_name} in {to_harness}")

    return ret_recs, errors

def post_process(data_list: List[str], columns: List[str]) -> List[str]:
    """
        Make sure that each entry in data list is padded with spaces in between the first two
        and last two columns so that each row has the same number of columns as length of columns

        Params
        ------
            * data_list: list of lists of strings, each of which represents a row of data
            * columns: the comprehensive list of columns to appear in the output frame, which
                is used to parametrize the length of each row in data_list

        Return
        ------
            The data_list padded with spaces to match the number of columns in the columns input
    """
    num_cols = len(columns)
    counter = 0
    for row in data_list:
        row_len = len(row)
        if row_len < num_cols:
            tmp_row = row[:row_len-2] + [""]*(num_cols - row_len) + row[row_len-2:]
            data_list[counter] = tmp_row
        counter += 1

    return data_list

def create_report_cache(conn, data_list: List[List[str]], columns: List[str]):
    """
        Create a cache for the report if cache is invalid. If the cache is valid, then
        do nothing.

        Params
        ------
            * conn: psycopg2 connection object
            * data_list: a list of rows of data to be inserted in cache is invalidated
            * columns: list of column names so that we can construct the table schema for the report
                cache if need be
    """
    col_info = {x: "text" for x in columns}
    table_name = "report_cache"

    is_valid = cache_is_valid(conn)

    # only write a new cache if the current cache is invalid
    if is_valid is False:
        dh.drop_table(conn=conn, table_name=table_name)
        dh.create_table(conn=conn, table_name=table_name, column_info=col_info)
        records_list = [dict(zip(columns, x)) for x in data_list]
        dh.insert_records(conn=conn, table_name=table_name, records_list=records_list)
        date_time_today = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        dh.upsert_records(
            conn=conn,
            table_name="ingestion_info",
            conflict_col="table_name",
            records_list=[
                {"table_name": table_name, "ingestion_date": date_time_today, "ingestion_success": True}
            ]
        )

def cache_is_valid(conn) -> bool:
    """
        Check cache validity. If the cache is older than ingestion date of any harness
        table then return false, otherwise return true.

        Params
        ------
            * conn: psycopg2 connection object to the database
            * last_cache_date: the most recent date when the cache was written
            * table_name: the name of the report cache table

        Return
        ------
            * is_valid: true if the table is newer than any ingested harness table, and false
                otherwise
    """
    table_name = "report_cache"

    harness_ingestion_recs = dh.select_with_where(
        conn=conn,
        table_name="ingestion_info",
        cols=["table_name", "ingestion_date"]
    )

    last_ingestion_date = max(
        [
            x["ingestion_date"] for x in harness_ingestion_recs if x["table_name"] != table_name
        ]
    )
    cache_date_info = [x["ingestion_date"] for x in harness_ingestion_recs if x["table_name"] == table_name]

    if not cache_date_info:
        return False
    else:
        last_cache_date = cache_date_info[0]

    if last_ingestion_date > last_cache_date:
        return False
    else:
        return True


def main(input_tables: List[str], output_file: str, diff_output_file: str, skip_cache: bool=False):
    """
        given a list of input tables, trace all unique signals through
        the harnesses and output a report as a .xlsx file

        Params
        ------
            * input_tables: list of input table names, i.e. the harness tables from which
                the signals eminate
            * output_file: path to write the resulting report
    """
    conn = dh.get_conn()

    cache_table_name = "report_cache"
    if skip_cache is True:
        valid_cache = False
    else:
        valid_cache = cache_is_valid(conn)

    try:
        cache_recs = dh.select_with_where(
            conn, 
            table_name=cache_table_name
        )
        columns = list(cache_recs[0].keys())
        data_list = [
            list(x.values()) for x in cache_recs
        ]
    except Exception:
        conn.rollback()
        data_list = []
        columns = None

    old_data_list = None

    if valid_cache is True:
        print("Cache is valid, generating report from cached report...")
    else:
        old_data_list = data_list
        old_columns = columns

        harness_tables = dh.select_with_where(
            conn,
            table_name="information_schema.tables",
            cols=["table_name"],
            wheres={"table_schema": ("=", "public")}
        )

        harness_tables = [x["table_name"] for x in harness_tables]

        output_schema_path = get_output_columns_path()
        output_schema = read_yaml(output_schema_path)
        if output_schema is None:
            raise Exception(f"There is no output schema at {output_schema_path}. Please fix!")

        start_columns = output_schema.get("start_columns")
        core_columns = output_schema.get("core_columns")
        end_columns = output_schema.get("end_columns")
        if any([x is None for x in [start_columns, core_columns, end_columns]]):
            raise Exception(
                "One of 'base_columns', 'core_columns', 'end_columns'"
                f"missing from the output schema file located at {output_schema_path}. Please fix!"
            )

        data_list = []

        select_col_schema_path = get_select_columns_path()
        select_cols = read_yaml(select_col_schema_path)

        for input_table in input_tables:
            print(f"processing input table {input_table}...")

            cols = list(select_cols.values())
            source_recs = dh.select_with_where(conn, input_table, cols=cols)

            target_key = select_cols["target"]
            source_key = select_cols["source"]

            target_names = list(set([x[target_key] for x in source_recs]))
            source_names = list(set([x[source_key] for x in source_recs]))
            source_only_recs = [x for x in source_recs if x[source_key] not in target_names]

            for rec in source_only_recs:
                tmp_data_lst, errors = process_record(conn, rec, source_names, harness_tables, cols)
                
                for tmp_data in tmp_data_lst:
                    signal_net_name = rec.get(select_cols.get("signal_net_name", ""), "")
                    cdh_pin = rec.get(select_cols.get("cdh_pin", ""), "")
                    error_flag = "false"
                    error_str = ""
                    if len(errors) > 0:
                        error_flag = "true"
                        error_str = "; ".join(list(set(errors)))
                    tmp_data += [signal_net_name, cdh_pin, error_flag, error_str]
                    data_list.append(tmp_data)

        num_to_add = int((max([len(x) for x in data_list]) - len(end_columns) - 1)/len(core_columns))
        columns = start_columns

        # add indexing on column names
        for i in range(num_to_add):
            tmp_core_columns = [x.replace("$", f"{i+1}") for x in core_columns]
            columns += tmp_core_columns
        columns += end_columns

        # post process the data list. We need to potentially add blank columns to each row
        print("post processing...")
        data_list = post_process(data_list, columns)

        # create a table with schema defined by columns object, and write data from data_list
        # into the table to be used as a cache for reporting
        print("Checking cache and creating if invalid")
        create_report_cache(conn=conn, data_list=data_list, columns=[x.lower() for x in columns])

    df = pd.DataFrame(data_list, columns=columns)
    df.to_csv(output_file, index=False)

    if old_data_list is not None:
        if old_columns is None:
            old_columns = columns
        old_df = pd.DataFrame(old_data_list, columns=old_columns)
        old_df.sort_values(by="harness_net_name", ignore_index=True, inplace=True)
        df.sort_values(by="harness_net_name", ignore_index=True, inplace=True)
        merged = old_df.merge(df, indicator=True, how="outer")
        diff_df = merged.loc[merged["_merge"] != "both"]
        diff_df.to_csv(diff_output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", default="./output/test_output.csv")
    parser.add_argument("--diff_output_file", default="./output/diff_output.csv")
    parser.add_argument("--skip_cache", action="store_true")
    args = parser.parse_args()

    source_tables_path = get_source_tables_path()
    source_tables = read_yaml(source_tables_path)["table_names"]

    main(
        input_tables=source_tables,
        output_file=args.output_file,
        diff_output_file=args.diff_output_file,
        skip_cache=args.skip_cache
    )
