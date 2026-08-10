from pathlib import Path
import logging

Path("data/processed").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("data/processed/log.txt"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("pipeline")

class ReadError(Exception): pass
class CleanError(Exception): pass
class ExportError(Exception): pass

class Pipeline:
    def run(self, filepath: str):
        from . import processors
        try:
            log.info(f"[1/3] READER -> {filepath}")
            df = processors.read(filepath)
            log.info(f"[2/3] CLEANER -> {len(df)} filas")
            df = processors.clean(df)
            log.info(f"[3/3] EXPORTER")
            out = processors.export(df)
            log.info(f"OK -> {out}")
            return out
        except Exception as e:
            log.error(f"FALLO: {e}")
            raise
