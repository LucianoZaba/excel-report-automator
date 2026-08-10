import sqlite3
from pathlib import Path
import pandas as pd

DB_DEFAULT = "data/processed/reporte.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    producto TEXT,
    cantidad INTEGER,
    precio REAL,
    total REAL,
    fecha_proceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_connection(db_path: str = DB_DEFAULT):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)

def init_db(db_path: str = DB_DEFAULT):
    conn = get_connection(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    return db_path

def save_df_to_db(df: pd.DataFrame, db_path: str = DB_DEFAULT, table: str = "ventas"):
    """Guarda DataFrame limpio en SQLite para reporting."""
    conn = get_connection(db_path)
    init_db(db_path)
    # Solo guarda columnas relevantes si existen
    df_to_save = df.copy()
    if 'total' not in df_to_save.columns and 'cantidad' in df_to_save.columns and 'precio' in df_to_save.columns:
        try:
            df_to_save['total'] = df_to_save['cantidad'] * df_to_save['precio']
        except:
            pass
    
    df_to_save.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()
    return db_path
