import os

def test_schema_path():
    schema_path = f"{os.path.dirname(__file__)}/../config/harness_schema.yaml"
    assert os.path.exists(schema_path)