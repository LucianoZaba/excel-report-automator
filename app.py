import argparse
from pathlib import Path
from src.pipeline import Pipeline

def pedir_excel_entrada(default_arg):
    # Si pasaron un path valido por argumento, usarlo
    if default_arg:
        p = Path(default_arg)
        if p.exists():
            return p
    
    # Buscar excels en data/raw
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    excels = list(raw_dir.glob("*.xlsx")) + list(raw_dir.glob("*.xls")) + list(raw_dir.glob("*.csv"))
    
    print("\n=== Excel Report Automator ===\n")
    
    if excels:
        print("Encontre estos archivos en data/raw/:")
        for i, f in enumerate(excels, 1):
            print(f"  {i}. {f.name}")
        print(f"  0. Ingresar otra ruta manualmente\n")
    
    while True:
        if excels:
            resp = input("Elegi numero o arrastra tu Excel aca (Enter para usar el primero): ").strip().replace('"','').replace("'","")
            if resp == "":
                return excels[0]
            if resp.isdigit():
                idx = int(resp)
                if idx == 0:
                    pass # pedir ruta
                elif 1 <= idx <= len(excels):
                    return excels[idx-1]
                else:
                    print("Numero invalido")
                    continue
            # si no es numero, asumir que es path
            p = Path(resp)
            if p.exists():
                return p
            else:
                print(f"No existe: {p}")
        else:
            resp = input("Arrastra tu Excel aca o pega la ruta: ").strip().replace('"','').replace("'","")
            p = Path(resp)
            if p.exists():
                return p
            print(f"No existe: {p}. Intenta de nuevo.")

def pedir_nombre_salida(output_arg):
    if output_arg and output_arg != "data/processed/reporte_limpio.xlsx":
        # Si usuario paso -o por terminal, respetarlo
        return Path(output_arg)
    
    print("\n--- Guardado ---")
    nombre = input("Nombre para el reporte limpio (solo nombre, sin .xlsx) [reporte_limpio]: ").strip()
    
    if not nombre:
        nombre = "reporte_limpio"
    
    # Sacar extension si la escribio y sanitizar
    nombre = nombre.replace(".xlsx","").replace(".xls","").replace(".csv","").strip()
    # Evitar caracteres invalidos
    nombre = "".join(c for c in nombre if c.isalnum() or c in ('_','-',' ')).strip()
    if not nombre:
        nombre = "reporte_limpio"
    
    return Path(f"data/processed/{nombre}.xlsx")

def main():
    parser = argparse.ArgumentParser(description="Excel Report Automator")
    parser.add_argument("input", nargs="?", default=None, help="Ruta al Excel de entrada")
    parser.add_argument("-o", "--output", default=None, help="Ruta de salida (opcional)")
    parser.add_argument("--db", action="store_true", help="Guardar tambien en SQLite")
    args = parser.parse_args()

    input_path = pedir_excel_entrada(args.input)
    output_path = pedir_nombre_salida(args.output)

    print(f"\nProcesando: {input_path} -> {output_path}")

    pipeline = Pipeline()
    try:
        result = pipeline.run(str(input_path), str(output_path), save_to_db=args.db)
        print(f"\n✅ Reporte generado: {result}")
        if args.db:
            print(f"✅ Base de datos: data/processed/reporte.db (modo append, historico conservado)")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
