import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import RealDictCursor
from typing import Any, Dict, List

from dotenv import load_dotenv
import os

def get_conn(host="ema-harness-db", user="ema_mgr", dbname="harness"):
    load_dotenv()
    password = os.environ["HARNESS_DB_PASSWORD"]
    conn = psycopg2.connect(host=host, user=user, password=password, dbname=dbname)
    return conn

def create_table(conn, table_name: str, column_info: dict):
    """
        Create a table using the database connection named table_name
        and with schema specified by column_info

        Params
        ------
            * conn: the psycopg2 connection instance used to establish connection
                to the database
            * table_name: the name of the table we wish to create
            * column_info: dict keyed by column name with values as the column type
    """
    columns = ",".join([f'"{x}" {column_info[x]}' for x in column_info])
    cur = conn.cursor()
    sql = f"""create table if not exists {table_name}({columns})"""
    cur.execute(sql)
    conn.commit()

def insert_records(conn, table_name: str, records_list: List[Dict[str, Any]]):
    """
        Given a list of dictionaries keyed by column name with values as the value for that entry
        in that respective column, insert those records into the desired table.

        Params
        ------
            * conn: the psycopg2 connection object that we will use to create a database cursor
            * table_name: the name of the table to which we will be writing
            * records_list: list of dictionaries keyed by column name with values as the value
                of that entry for that column
    """
    # for now, since we do not have primary keys in the harness schema, we are just going to
    # delete all records and insert new ones if the table exists
    if table_exists(conn, table_name):
        delete_from_table(conn, table_name)

    cur = conn.cursor()
    print(f"Attempting to insert {len(records_list)} rows into {table_name}...")
    inserted = 0
    # Note: we could query for the existing hashes in the table for the current bill cycle
    # and then filter on those from records_list to omit duplicate writes. We could then batch
    # insert all records whose hash does not appear, which would be significantly faster than looping
    # as we do here. That is an optimization. And optimizations are for the future. To the future!
    for record in records_list:
        columns = [f'"{x}"' for x in record.keys()]
        values = record.values()
        sql = """
            insert into %s (%s) values %s
        """
        # AsIs will escape single quotes around identifiers such as table and column names.
        # we mogrify the strings to prevent against injection here.
        formatted_sql = cur.mogrify(sql, (AsIs(table_name), AsIs(",".join(columns)), tuple(values)))
        cur.execute(formatted_sql)
        inserted += 1
        conn.commit()

    print(f"Inserted: {inserted}")
    conn.commit()

def delete_from_table(conn, table_name: str):
    """
        Delete all records from table with given name

        Params
        ------
            * conn: psycopg2 connection object
            * table_name: string representing the name of the table we wish to delete from
    """
    print(f"Deleting records from {table_name}...")
    cur = conn.cursor()
    sql = """
        delete from %s
    """
    formatted_sql = cur.mogrify(sql, (AsIs(table_name),))
    cur.execute(formatted_sql)
    conn.commit()

def table_exists(conn, table_name: str):
    """
        Determine if the table with the given name exists in the database 
        specified by the connection object

        Params
        ------
            * conn: psycopg2 connection object
            * table_name: string representing the name of the table, the existence
                of which we are interested in
    """
    print(f"Checking for existence of {table_name}...")
    cur = conn.cursor()
    sql = """
        select table_name from information_schema.tables where table_schema = 'public';    
    """
    cur.execute(sql)
    table_names = cur.fetchall()
    table_names = [x[0] for x in table_names]
    if table_name in table_names:
        return True
    else:
        return False
    
def drop_table(conn, table_name: str):
    """
        Drop the table with the given name if it exists from the database
        specified by the connection object

        Params
        ------
            * conn: psycopg2 connection object
            * table_name: string representing the name of the table we wish to drop
    """
    print(f"Dropping {table_name}...")
    cur = conn.cursor()
    sql = """
        drop table if exists %s
    """
    formatted_sql = cur.mogrify(sql, (AsIs(table_name),))
    cur.execute(formatted_sql)
    conn.commit()

def select_with_where(
    conn, 
    table_name: str,
    wheres: Dict[str, Any] = None,
    cols: List[str] = None,
    groupers: List[str] = None
) -> List[Dict[str, Any]]:
    """
        Select optional columns, or * if no columns passed, from the table with the given name
        filtered based on the list of wheres and associated vals

        Params
        ------
            * conn: psycopg2 connection object to a postgresql database
            * table_name: name of a table in the postgresql database held by the connection
            * wheres: optional dict keyed by column name with value as column value to filter on
            * cols: optional list of column names to select from the table. Select * if none passed. Default = None
        
        Return
        ------
            * records: list of dicts, each representing a row with the selected columns from the query
    """
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # add quotes around column names because of keyworded column names
    # cols = [f'"{x}"' for x in cols]

    if cols is None:
        select_cols = AsIs("*")
    else:
        select_cols = AsIs(",".join(cols))

    if wheres is not None:
        where = AsIs(" and ".join(
                [
                    f"{x} {wheres[x][0]} '{wheres[x][1]}'"
                    if type(wheres[x][1]) != tuple else f"{x} {wheres[x][0]} {wheres[x][1]}"
                    for x in wheres
                ]
            )
        )
        if groupers is not None:
            groups = AsIs(",".join(groupers))
            sql = """
                select %s from %s where %s group by %s
            """
            query = cur.mogrify(sql, (select_cols, AsIs(table_name), where, groups,))
        else:
            sql = """
                select %s from %s where %s
            """
            query = cur.mogrify(sql, (select_cols, AsIs(table_name), where,))
    else:
        if groupers is not None:
            groups = AsIs(",".join(groupers))
            sql = """
                select %s from %s group by %s
            """
            query = cur.mogrify(sql, (select_cols, AsIs(table_name), groups))
        else:
            sql = """
                select %s from %s
            """
            query = cur.mogrify(sql, (select_cols, AsIs(table_name),))

    cur.execute(query)
    conn.commit()
    records = cur.fetchall()
    return records
