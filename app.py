import argparse
from pathlib import Path
from src.pipeline import Pipeline

def main():
    parser = argparse.ArgumentParser(description="Excel Report Automator - Automatiza limpieza y reportes de Excel")
    parser.add_argument("input", nargs="?", default="data/raw/ejemplo.xlsx", help="Ruta al Excel de entrada (default: data/raw/ejemplo.xlsx)")
    parser.add_argument("-o", "--output", default="data/processed/reporte_limpio.xlsx", help="Ruta de salida")
    parser.add_argument("--db", action="store_true", help="Guardar tambien en SQLite")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[!] No existe: {input_path}")
        print(f"    Crea un archivo de prueba en data/raw/ejemplo.xlsx")
        print(f"    Columnas sugeridas: cliente, producto, cantidad, precio")
        return

    pipeline = Pipeline()
    result = pipeline.run(str(input_path), args.output, save_to_db=args.db)
    print(f"✅ Reporte generado: {result}")

if __name__ == "__main__":
    main()
