import pyodbc
from .config import DATABASE_CONFIG

def get_db_connection():
    conn_str = (
        f"DRIVER={{{DATABASE_CONFIG['driver']}}};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']}"
    )
    connection = pyodbc.connect(conn_str)
    return connection
