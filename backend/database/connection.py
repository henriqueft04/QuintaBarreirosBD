import pyodbc
from .config import DATABASE_CONFIG
from flask import g

def get_db_connection():
    if 'db' not in g:
        g.db = pyodbc.connect(
        f"DRIVER={{{DATABASE_CONFIG['driver']}}};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']}"
    )

    return g.db

def close_db_connection():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db_connection)

    with app.app_context():
        db = get_db_connection()
        db.commit()
