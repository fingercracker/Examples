from database_handler import select_with_where
from file_utils import get_select_columns_path, read_yaml
from generate_report import process_record

def test_process_record_interconnect(conn):
    """
        Table h1 is a source table while h2 contains an interconnect as a source connector.
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

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
        cols=cols
    )

    table_names = [x["table_name"] for x in table_recs]
    source_names = [x[select_cols["source"]] for x in recs]
    
    # select the desired signal
    rec = [x for x in recs if x[select_cols["harness_net_name"]] == "SOME_SIGNAL_NAME_1"][0]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [[
        'SOME_SIGNAL_NAME_1', 'RWA1-P2', '15', 'H2-H1-J1', '4', 'H2', 'M27500A22SR2U00', 'H2-H1-P1', '4', 'PCUSC1-P1', '2', 'H1', 'M27500A22SR2U00'
    ]]
    assert errors == []


def test_same_signal_wiretype_mismatch(conn):
    """
        SOME_SIGNAL_NAME_2 appears correctly across H1 to H2, but has the wrong wiretype in H2
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

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
        cols=cols
    )

    table_names = [x["table_name"] for x in table_recs]
    source_names = [x[select_cols["source"]] for x in recs]
    
    # select the desired signal
    rec = [x for x in recs if x[select_cols["harness_net_name"]] == "SOME_SIGNAL_NAME_2"][0]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [[
        'SOME_SIGNAL_NAME_2', 'RWA1-P2', '14', 'H2-H1-J1', '3', 'H2', 'M27500A22SR2U01', 'H2-H1-P1', '3', 'PCUSC1-P1', '4', 'H1', 'M27500A22SR2U00'
    ]]
    assert errors == ['Wire type mismatch in harness h2 for signal SOME_SIGNAL_NAME_2']


def test_same_signal_pin_mismatch(conn):
    """
        SOME_SIGNAL_NAME_3 has a pin mismatch between h1 and h2
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

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
        cols=cols
    )

    table_names = [x["table_name"] for x in table_recs]
    source_names = [x[select_cols["source"]] for x in recs]
    
    # select the desired signal
    rec = [x for x in recs if x[select_cols["harness_net_name"]] == "SOME_SIGNAL_NAME_3"][0]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [[
        'SOME_SIGNAL_NAME_3', 'H2-H1-P1', '20', 'PCUSC1-P1', '4', 'H1', 'M27500A22SR2U00'
    ]]
    assert errors == ['Signal SOME_SIGNAL_NAME_3 is not assigned to pin 20 on harness h2']


def test_missing_signal_name(conn):
    """
        SOME_SIGNAL_NAME_4 appears in h1 and goes through interconnect to h2, but does
        not appear in h2.
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

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
        cols=cols
    )

    table_names = [x["table_name"] for x in table_recs]
    source_names = [x[select_cols["source"]] for x in recs]
    
    # select the desired signal
    rec = [x for x in recs if x[select_cols["harness_net_name"]] == "SOME_SIGNAL_NAME_4"][0]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [[
        'SOME_SIGNAL_NAME_4', 'H2-H1-P1', '3', 'PCUSC1-P1', '4', 'H1', 'M27500A22SR2U00'
    ]]
    assert errors == ['There is no signal SOME_SIGNAL_NAME_4 in harness table h2']


def test_process_record_arm_plug(conn):
    """
        test table h3 has an arm plug with a single signal going through that arm plug. Verify
        that the signal self joins correctly
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

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
        cols=cols
    )

    table_names = [x["table_name"] for x in table_recs]
    target_names = [x[select_cols["target"]] for x in recs]
    source_names = [x[select_cols["source"]] for x in recs]
    source_only_recs = [x for x in recs if x[select_cols["source"]] not in target_names]

    rec = source_only_recs[0]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [[
        'SOME_SIGNAL_NAME_3', 'XFC-P1', '2', 'XFC-ARM-J1', '3', 'H3', 'ABC1234', 'XFC-ARM-J1', '14', 'FTSU-P09', '4', 'H3', 'ABC1234'
    ]]

    assert errors == []


def test_process_records_arm_plug_multiple_times_error(conn):
    """
        test table h4 has an arm plug with a signal that appears multiple times
        from the same connector.
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

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
        table_name="h4",
        cols=cols
    )

    table_names = [x["table_name"] for x in table_recs]
    target_names = [x[select_cols["target"]] for x in recs]
    source_names = [x[select_cols["source"]] for x in recs]
    source_only_recs = [x for x in recs if x[select_cols["source"]] not in target_names]

    rec = [x for x in source_only_recs if x[select_cols["harness_net_name"]] == "SOME_SIGNAL_NAME_4"][0]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [
        ['SOME_SIGNAL_NAME_4', 'XFC-P1', '2', 'XFC-ARM-J1', '3', 'H4', 'ABC1234', 'XFC-ARM-J1', '14', 'FTSU-P09', '4', 'H4', 'ABC1234'],
        ['SOME_SIGNAL_NAME_4', 'XFC-P1', '10', 'XFC-ARM-J1', '5', 'H4', 'ABC1234', 'XFC-ARM-J1', '14', 'FTSU-P09', '4', 'H4', 'ABC1234']
    ]

    assert errors == ['Signal SOME_SIGNAL_NAME_4 appears multiple times in H4 from connector XFC-ARM-J1']


def test_process_records_arm_plug_missing_signal(conn):
    """
        test table h4 has an arm plug with a signal that dead ends.
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

    table_recs = select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={
            "table_schema": ("=", "public")
        }
    )
    table_names = [x["table_name"] for x in table_recs]

    recs = select_with_where(
        conn,
        table_name="h4",
        cols=cols
    )
    source_names = list(set([x[select_cols["source"]] for x in recs]))

    # Choose the signal name that only appears once for the sake of this test
    [rec] = [x for x in recs if x[select_cols["harness_net_name"]] == "SOME_SIGNAL_NAME_N"]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    # we extract the info for this one appearance of this signal, but then it terminates
    assert processed_records == [[
        'SOME_SIGNAL_NAME_N', 'XFC-ARM-J1', '1', 'FTSU-P09', '7', 'H4', 'ABC1234'
    ]]

    # the target harness for SOME_SIGNAL_NAME_N appears in the source column, but there
    # is no corresponding signal name with that connector in the source column, which must
    # mean that it (potentially) terminates early
    assert errors == ['Signal SOME_SIGNAL_NAME_N terminates prematurely in harness H4']

def test_process_records_test_plug(conn):
    """
        test table h6 has a test plug for a signal originating from test table h1.
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

    table_recs = select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={
            "table_schema": ("=", "public")
        }
    )
    table_names = [x["table_name"] for x in table_recs]

    recs = select_with_where(
        conn,
        table_name="h1",
        cols=cols
    )
    source_names = list(set([x[select_cols["source"]] for x in recs]))

    [rec] = [x for x in recs if x[select_cols["harness_net_name"]] == "TEST_PLUG_SIGNAL"]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [
        ['TEST_PLUG_SIGNAL', 'P49-P1', '26', 'SP6', 'B', 'H5', 'M22759/44-20-9', 'SP6', 'A', 'H5-H1-J1', 'F', 'H5', 'M22759/44-20-9', 'H5-H1-P1', 'F', 'Something', '103', 'H1', 'M22759/44-20-9'],
        ['TEST_PLUG_SIGNAL', 'PRP-TEST-J1', '5', 'SP6', 'B', 'H5', 'M22759/44-20-9', 'SP6', 'A', 'H5-H1-J1', 'F', 'H5', 'M22759/44-20-9', 'H5-H1-P1', 'F', 'Something', '103', 'H1', 'M22759/44-20-9']
    ]

    assert errors == []

def test_process_records_splice(conn):
    """
        test table h6 has a splice from a signal originating in test table h1.
    """
    select_cols = read_yaml(get_select_columns_path())
    cols = list(select_cols.values())

    table_recs = select_with_where(
        conn,
        table_name="information_schema.tables",
        cols=["table_name"],
        wheres={
            "table_schema": ("=", "public")
        }
    )
    table_names = [x["table_name"] for x in table_recs]

    recs = select_with_where(
        conn,
        table_name="h1",
        cols=cols
    )
    source_names = list(set([x[select_cols["source"]] for x in recs]))

    [rec] = [x for x in recs if x[select_cols["harness_net_name"]] == "SPLICE_SIGNAL"]

    processed_records, errors = process_record(conn, rec, source_names, table_names, cols)

    assert processed_records == [
        ['SPLICE_SIGNAL', 'P702-P1', '11', 'SP13', 'B', 'H6', 'M22759/33-26-9', 'SP13', 'A', 'H6-H1-J1', 'S', 'H6', 'M27500-20SR2S23', 'H6-H1-P1', 'S', 'BlaBla', '104', 'H1', 'M27500-20SR2S23'],
        ['SPLICE_SIGNAL', 'P702-P1', '23', 'SP13', 'B', 'H6', 'M22759/33-26-9', 'SP13', 'A', 'H6-H1-J1', 'S', 'H6', 'M27500-20SR2S23', 'H6-H1-P1', 'S', 'BlaBla', '104', 'H1', 'M27500-20SR2S23'],
        ['SPLICE_SIGNAL', 'P702-P1', '7', 'SP13', 'B', 'H6', 'M22759/33-26-9', 'SP13', 'A', 'H6-H1-J1', 'S', 'H6', 'M27500-20SR2S23', 'H6-H1-P1', 'S', 'BlaBla', '104', 'H1', 'M27500-20SR2S23'],
        ['SPLICE_SIGNAL', 'P702-P1', '19', 'SP13', 'B', 'H6', 'M22759/33-26-9', 'SP13', 'A', 'H6-H1-J1', 'S', 'H6', 'M27500-20SR2S23', 'H6-H1-P1', 'S', 'BlaBla', '104', 'H1', 'M27500-20SR2S23']
    ]

    assert list(set(errors)) == ['Wire type mismatch in harness h6 for signal SPLICE_SIGNAL']
