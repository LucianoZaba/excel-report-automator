from pathlib import Path
import logging

# Crear carpeta de logs antes del handler
Path("data/processed").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler("data/processed/log.txt", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("pipeline")

class ReadError(Exception): pass
class CleanError(Exception): pass
class ExportError(Exception): pass

class Pipeline:
    """Orquestador central: Reader -> Cleaner -> Exporter -> (opcional) DB"""
    
    def run(self, filepath: str, output_path: str = "data/processed/reporte_limpio.xlsx", save_to_db: bool = False):
        from . import processors
        from . import database

        try:
            log.info(f"[1/3] READER -> {filepath}")
            df = processors.read(filepath)

            log.info(f"[2/3] CLEANER -> {len(df)} filas iniciales")
            df_clean = processors.clean(df)
            log.info(f"       -> {len(df_clean)} filas finales")

            log.info(f"[3/3] EXPORTER -> {output_path}")
            out = processors.export(df_clean, output_path)
            
            if save_to_db:
                log.info(f"[EXTRA] DB -> SQLite")
                database.save_df_to_db(df_clean)

            log.info(f"OK -> {out}")
            return out

        except Exception as e:
            log.error(f"FALLO en {type(e).__name__}: {e}")
            raise
