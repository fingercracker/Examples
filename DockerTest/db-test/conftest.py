import pytest
from database_handler import get_conn

@pytest.fixture
def conn():
    return get_conn(
        host="0.0.0.0",
        dbname="postgres",
        user="test_user",
        password="test_password_1234"
    )