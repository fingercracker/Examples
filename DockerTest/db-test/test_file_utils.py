import os
import file_utils

def test_schema_path():
    schema_path = os.path.join(f"{os.path.dirname(__file__)}", "config", "harness_schema.yaml")
    assert os.path.exists(schema_path)

def test_read_yaml():
    test_path = f"{os.path.dirname(__file__)}/test_config.yaml"
    test_dict = file_utils.read_yaml(test_path)
    assert test_dict == {"test_thing": ["this", "is", "a", "test"]}

def test_read_yaml_no_path():
    test_path = "this/is/not/a/path"
    none_dict = file_utils.read_yaml(test_path)
    assert none_dict == None
