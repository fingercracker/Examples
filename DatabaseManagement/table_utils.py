from typing import List


def get_primary_keys(conn, table_name: str) -> List[str]:
    """
        Collect the column names that comprise the primary key for the table with the given name

        Params
        ------
            * table_name: name of the table whose primary keys we want

        Return
        ------
            * pkeys: a list of strings representing the column names that comprise the primary key
    """
    cur = conn.cursor()

    sql = """
        SELECT a.attname                                                   
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                            AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = %s::regclass
        AND    i.indisprimary;
    """

    query = cur.mogrify(sql, (table_name,))

    cur.execute(query)

    pkeys = cur.fetchall()
    pkeys = [x[0] for x in pkeys]
    return pkeys