import psycopg2
from psycopg2.extensions import AsIs
from typing import Any, Dict, List, Tuple
import table_utils


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
    columns = ",".join([f"{x} {column_info[x]}" for x in column_info])
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
    cur = conn.cursor()
    print(f"Attempting to insert {len(records_list)} rows into {table_name}...")
    inserted = 0
    updated = 0
    # Note: we could query for the existing hashes in the table for the current bill cycle
    # and then filter on those from records_list to omit duplicate writes. We could then batch
    # insert all records whose hash does not appear, which would be significantly faster than looping
    # as we do here. That is an optimization. And optimizations are for the future. To the future!
    for record in records_list:
        columns = record.keys()
        values = record.values()
        sql = """
            insert into %s (%s) values %s
        """
        # AsIs will escape single quotes around identifiers such as table and column names.
        # we mogrify the strings to prevent against injection here.
        formatted_sql = cur.mogrify(sql, (AsIs(table_name), AsIs(",".join(columns)), tuple(values)))
        try:
            cur.execute(formatted_sql)
            inserted += 1
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            pkeys = table_utils.get_primary_keys(conn, table_name)
            sql = """
                update %s
                set %s
                where %s
            """
            non_keys = [x for x in columns if x not in pkeys]
            for x in non_keys:
                if type(record[x]) == str:
                    record[x] = record[x].replace("'", "")
            set_clause = AsIs(",".join([f"{x} = '{record[x]}'" for x in non_keys]))
            where_clause = AsIs(" and ".join([f"{x} = '{record[x]}'" for x in pkeys]))

            query = cur.mogrify(sql, (AsIs(table_name), set_clause, where_clause))

            cur.execute(query)
            updated += 1
            conn.commit()

    print(f"Inserted: {inserted}\nUpdated: {updated}")
    conn.commit()
