import sqlite3
from pathlib import Path

def init_db(db_path="data/processed/reporte.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS ventas (id INTEGER, cliente TEXT, producto TEXT, cantidad INTEGER, precio REAL)")
    conn.commit()
    return conn
