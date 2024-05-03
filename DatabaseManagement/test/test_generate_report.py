from DatabaseManagement.utils.database_handler import get_conn, select_with_where
from DatabaseManagement.jobs.generate_report import process_record

def test_process_record_interconnect():
    """
        Table h1 is a source table while h2 contains an interconnect as a source connector.

    """
    conn = get_conn(
        host="0.0.0.0",
        dbname="postgres",
        user="test_user",
        password="test_password_1234"
    )

    table_recs = select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={
            "table_schema": ("=", "public")
        }
    )

    recs = select_with_where(
        conn,
        table_name="h1",
        wheres={
            "net": ("=", "SOME_SIGNAL_NAME_1")
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

def test_process_record_arm_plug():
    """
        test table h3 has an arm plug with a single signal going through that arm plug. Verify
        that the signal self joins correctly
    """
    conn = get_conn(
        host="0.0.0.0",
        dbname="postgres",
        user="test_user",
        password="test_password_1234"
    )

    table_recs = select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={
            "table_schema": ("=", "public")
        }
    )

    recs = select_with_where(
        conn,
        table_name="h3",
        wheres={
            "net": ("=", "SOME_SIGNAL_NAME_3")
        }
    )

    table_names = [x["table_name"] for x in table_recs]
    target_names = [x["target"] for x in recs]
    source_names = [x["source"] for x in recs]
    source_only_recs = [x for x in recs if x["source"] not in target_names]
    
    rec = source_only_recs[0]

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
        'SOME_SIGNAL_NAME_3', 'H3', 'FTSU-P09', '4', 'H3', 'XFC-ARM-J1', '20', 'H3', 'XFC-ARM-J1', '2', 'H3', 'XFC-P1', '10'
    ]
