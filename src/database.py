import sqlite3
from pathlib import Path
import pandas as pd

DB_DEFAULT = "data/processed/reporte.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS ventas (
    id REAL,
    cliente TEXT,
    producto TEXT,
    categoria TEXT,
    cantidad REAL,
    precio_unitario REAL,
    precio REAL,
    descuento REAL,
    total REAL,
    fecha TIMESTAMP,
    vendedor TEXT,
    sucursal TEXT,
    estado TEXT,
    cuit TEXT,
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

def save_df_to_db(df: pd.DataFrame, db_path: str = DB_DEFAULT, table: str = "ventas", mode: str = "append"):
    """
    Guarda DataFrame en SQLite.
    
    mode:
      - "append" (default): conserva historico, agrega sin borrar. Ideal para Workana.
      - "replace": reemplaza toda la tabla (comportamiento anterior)
    
    Si hay columna id, evita duplicar ids ya existentes.
    """
    conn = get_connection(db_path)
    init_db(db_path)
    
    df_to_save = df.copy()
    
    # Si modo append y hay id, evitar insertar ids que ya existen
    if mode == "append" and 'id' in df_to_save.columns:
        try:
            existing_ids = pd.read_sql(f"SELECT id FROM {table}", conn)['id'].tolist()
            before = len(df_to_save)
            df_to_save = df_to_save[~df_to_save['id'].isin(existing_ids)]
            if len(df_to_save) < before:
                print(f"[DB] {before - len(df_to_save)} registros con id ya existente ignorados (historico conservado)")
        except:
            pass # tabla vacia o no existe aun

    if_exists = "append" if mode == "append" else "replace"
    df_to_save.to_sql(table, conn, if_exists=if_exists, index=False)
    conn.close()
    return db_path
