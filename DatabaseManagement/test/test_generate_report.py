from DatabaseManagement.utils.database_handler import get_conn, select_with_where
from DatabaseManagement.jobs.generate_report import process_record

conn = get_conn(
    host="0.0.0.0",
    dbname="postgres",
    user="test_user",
    password="test_password_1234"
)

def test_process_record():
    recs = select_with_where(
        conn,
        table_name="h1",
        wheres={
            "net": ("=", "SOME_SIGNAL_NAME_1")
        }
    )

    table_recs = select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={
            "table_schema": ("=", "public")
        }
    )

    table_names = [x["table_name"] for x in table_recs]
    source_names = [x["source"] for x in recs]
    rec = recs[0]

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

    processed_records = process_record(conn, rec, source_names, table_names, cols)

    conn.close()

    assert processed_records == [
        'SOME_SIGNAL_NAME_1', 'H1', 'PCUSC1-P1', '1', 'H1', 'H2-H1-P1', '2', 'H2', 'H2-H1-J1', '2', 'H2', 'RWA1-P2', '10'
    ]

