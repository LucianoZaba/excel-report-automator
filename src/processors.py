import pandas as pd
from pathlib import Path
from openpyxl.styles import Font
from .pipeline import ReadError, CleanError, ExportError, log

def read(path: str) -> pd.DataFrame:
    """Lee Excel/CSV. Soporta .xlsx, .xls, .csv"""
    try:
        log.info(f"Leyendo {path}")
        p = Path(path)
        if p.suffix.lower() == '.csv':
            return pd.read_csv(path)
        return pd.read_excel(path)
    except Exception as e:
        raise ReadError(f"No se pudo leer {path}: {e}")

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza profesional para Workana."""
    try:
        # 1. Normaliza columnas: " Precio Unitario " -> "precio_unitario"
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        
        # 2. Limpia strings: "  Juan  " -> "Juan"
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({'nan': pd.NA, 'None': pd.NA, '': pd.NA})

        # 3. Elimina filas totalmente vacias
        df = df.dropna(how='all')
        
        # 4. Elimina duplicados exactos
        df = df.drop_duplicates()

        # 5. Intenta convertir numericos y calcular total
        for col in ['cantidad', 'precio', 'precio_unitario']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if 'cantidad' in df.columns and 'precio' in df.columns:
            df['total'] = df['cantidad'] * df['precio']
        elif 'cantidad' in df.columns and 'precio_unitario' in df.columns:
            df['total'] = df['cantidad'] * df['precio_unitario']

        # 6. Elimina filas con cantidad negativa o nula si aplica
        if 'cantidad' in df.columns:
            df = df[df['cantidad'] > 0]

        return df.reset_index(drop=True)

    except Exception as e:
        raise CleanError(f"Error limpiando datos: {e}")

def export(df: pd.DataFrame, output_path: str = "data/processed/reporte_limpio.xlsx") -> Path:
    """Exporta con formato profesional (headers en negrita, autofiltro)."""
    try:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardado inicial con pandas
        df.to_excel(out, index=False, sheet_name="Reporte")
        
        # Formateo extra con openpyxl
        try:
            from openpyxl import load_workbook
            wb = load_workbook(out)
            ws = wb["Reporte"]
            
            # Header en negrita
            for cell in ws[1]:
                cell.font = Font(bold=True)
            
            # Auto-filtro
            ws.auto_filter.ref = ws.dimensions
            
            # Ajuste ancho columnas
            for col in ws.columns:
                max_len = 0
                col_letter = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_len:
                            max_len = len(str(cell.value))
                    except:
                        pass
                ws.column_dimensions[col_letter].width = min(max_len + 2, 35)
            
            ws.freeze_panes = "A2"
            wb.save(out)
        except Exception as fmt_e:
            log.warning(f"No se pudo formatear con openpyxl: {fmt_e}")

        return out
    except Exception as e:
        raise ExportError(f"Error exportando a {output_path}: {e}")
