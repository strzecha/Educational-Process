from utils.database import create_connection

def test_create_connection():
    assert create_connection() is not None
