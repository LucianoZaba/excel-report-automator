Excel Report Automator

Automatizador de reportes de Excel con Python. Limpia, normaliza y genera reportes listos para enviar a clientes. Pensado para freelancers en Workana.

🚀 Que hace

Reader: Lee .xlsx, .xls, .csv desde data/raw/
Cleaner: Normaliza columnas, limpia espacios, elimina duplicados y vacíos, convierte tipos, calcula columna total
Exporter: Exporta a data/processed/reporte_limpio.xlsx con formato profesional (headers en negrita, autofiltros, columnas ajustadas, freeze)
DB (opcional): Guarda el resultado en SQLite para dashboards

🛠 Stack

Python 3.10+, Pandas, OpenPyXL, SQLite3, Logging

📁 Estructura

excel-report-automator/
├── app.py              # CLI principal
├── src/
│   ├── pipeline.py     # Orquestador + logs + errores custom
│   ├── processors.py   # read / clean / export
│   └── database.py     # SQLite opcional
├── data/
│   ├── raw/            # Excels de entrada (no se suben)
│   └── processed/      # Reportes generados + log.txt
└── requirements.txt

⚙️ Instalacion

git clone https://github.com/TU_USUARIO/excel-report-automator.git
cd excel-report-automator
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

▶️ Uso

Pone tu Excel sucio en data/raw/ejemplo.xlsx
Corre:

# Basico
python app.py

# Especificando archivos
python app.py data/raw/ventas.xlsx -o data/processed/ventas_limpio.xlsx

# Tambien guardar en SQLite
python app.py --db

Output: data/processed/reporte_limpio.xlsx + data/processed/log.txt

📊 Ejemplo de limpieza

Entrada: Columnas con espacios "  Precio ", duplicados, filas vacías
Salida: cliente | producto | cantidad | precio | total limpio, con formato

👨‍💻 Para Workana

Este repo demuestra:
Manejo de datos reales con Pandas
Codigo modular y con manejo de errores custom (ReadError, CleanError, ExportError)
Logging profesional para debugging
Buenas practicas de Git (.gitignore para datos sensibles)

Servicios que podes ofrecer con esto: Automatizacion de reportes, limpieza de bases de datos, conversion masiva de Excels, generacion de reportes mensuales automaticos.


MIT License - Luciano Zabaletta
