# Excel Report Automator

Automatizador de reportes de Excel desarrollado en Python. Permite leer archivos Excel o CSV, limpiar y normalizar los datos, calcular totales y generar un nuevo reporte Excel con formato profesional.

El proyecto está pensado como una herramienta de automatización de datos que puede adaptarse a distintos procesos de limpieza y generación de reportes.

---

## 🚀 ¿Qué hace?

El programa procesa un archivo de entrada mediante un pipeline dividido en etapas:

**Reader → Cleaner → Exporter → SQLite (opcional)**

### 📥 Reader

Lee archivos:

* `.xlsx`
* `.xls`
* `.csv`

El archivo de entrada se puede indicar desde la línea de comandos.

### 🧹 Cleaner

Realiza tareas de limpieza y normalización, entre ellas:

* Normalización de nombres de columnas.
* Eliminación de espacios innecesarios.
* Conversión de valores numéricos.
* Conversión de valores vacíos a valores nulos.
* Eliminación de filas completamente vacías.
* Eliminación de filas duplicadas.
* Eliminación de registros con cantidades menores o iguales a cero.
* Cálculo automático de la columna `total` cuando existen `cantidad` y `precio` o `precio_unitario`.

Las reglas pueden ampliarse según las necesidades de cada tipo de reporte.

### 📊 Exporter

Genera un nuevo archivo `.xlsx` con:

* Encabezados en negrita.
* Autofiltro.
* Ancho de columnas ajustado automáticamente.
* Primera fila congelada.
* Hoja denominada `Reporte`.

Por defecto se genera:

```text
data/processed/reporte_limpio.xlsx
```

### 🗄️ SQLite (opcional)

El resultado procesado puede guardarse también en una base de datos SQLite para utilizarlo posteriormente en consultas, análisis o dashboards.

Se activa mediante:

```bash
python app.py --db
```

---

## 🛠️ Tecnologías

* Python 3.10+
* Pandas
* OpenPyXL
* SQLite3
* Logging

---

## 📁 Estructura del proyecto

```text
excel-report-automator/
│
├── app.py
│
├── src/
│   ├── pipeline.py
│   ├── processors.py
│   └── database.py
│
├── data/
│   ├── raw/
│   │   └── # Archivos de entrada
│   │
│   └── processed/
│       ├── # Reportes generados
│       └── log.txt
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Responsabilidades

**`app.py`**
Punto de entrada de la aplicación y manejo de argumentos de línea de comandos.

**`pipeline.py`**
Coordina el flujo completo de procesamiento y centraliza los logs y errores.

**`processors.py`**
Contiene las funciones principales para leer, limpiar y exportar los datos.

**`database.py`**
Gestiona la persistencia opcional de los datos procesados en SQLite.

---

## ⚙️ Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/excel-report-automator.git
cd excel-report-automator
```

Crear un entorno virtual:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Uso

### Procesamiento básico

Colocar el archivo de entrada en:

```text
data/raw/ejemplo.xlsx
```

Ejecutar:

```bash
python app.py
```

El resultado se guardará en:

```text
data/processed/reporte_limpio.xlsx
```

### Especificar archivo de entrada y salida

```bash
python app.py data/raw/ventas.xlsx -o data/processed/ventas_limpio.xlsx
```

### Guardar también en SQLite

```bash
python app.py --db
```

También es posible combinar argumentos:

```bash
python app.py data/raw/ventas.xlsx -o data/processed/ventas_limpio.xlsx --db
```

---

## 📋 Ejemplo

Un archivo de entrada puede contener problemas como:

```text
" Cliente " | " Precio Unitario " | Cantidad
" Juan Perez " | 15000            | 2
" Maria "     | 25000            | -3
                 ...
```

Después del procesamiento, las columnas se normalizan y los datos inválidos según las reglas actuales son eliminados o convertidos.

El resultado puede quedar, por ejemplo:

```text
cliente      | precio_unitario | cantidad | total
Juan Perez   | 15000           | 2        | 30000
```

Además, el archivo Excel generado recibe formato para facilitar su lectura y utilización.

---

## 📝 Registro del proceso

El programa genera un archivo:

```text
data/processed/log.txt
```

El log permite conocer las diferentes etapas ejecutadas:

```text
[1/3] READER
[2/3] CLEANER
[3/3] EXPORTER
```

También registra errores durante la lectura, limpieza o exportación.

El proyecto utiliza excepciones específicas:

* `ReadError`
* `CleanError`
* `ExportError`

Esto facilita identificar en qué etapa ocurrió un problema.

---

## ⚠️ Consideraciones

El automatizador utiliza reglas generales de limpieza. La estructura y las reglas necesarias pueden variar según el Excel de cada cliente.

Por ejemplo, un reporte puede requerir reglas específicas para:

* columnas obligatorias;
* valores permitidos;
* fechas;
* estados;
* identificadores;
* descuentos;
* cálculos;
* duplicados.

Por este motivo, el proyecto está diseñado para poder adaptar la etapa `Cleaner` a diferentes necesidades.

---

## 💼 Aplicaciones profesionales

Este tipo de automatización puede utilizarse para:

* Limpieza de bases de datos en Excel.
* Automatización de reportes.
* Preparación de archivos para análisis.
* Conversión y normalización de datos.
* Generación de reportes periódicos.
* Preparación de información para dashboards.
* Procesamiento de grandes cantidades de registros.

### Ejemplo de servicio

Un cliente puede entregar un Excel con datos desordenados y solicitar:

1. Limpiar los registros.
2. Normalizar las columnas.
3. Eliminar datos inválidos o duplicados.
4. Realizar cálculos.
5. Generar un Excel final listo para utilizar.
6. Opcionalmente almacenar los datos en SQLite para posteriores análisis.

---

## 🎯 Objetivo del proyecto

El objetivo de **Excel Report Automator** es convertir tareas repetitivas de limpieza y preparación de datos en un proceso automatizado, reproducible y fácilmente adaptable a diferentes tipos de reportes.

---

## 📄 Licencia

MIT License - Luciano Zabaletta
