# Proyecto de Limpieza de Pandas — Entregable

Este directorio contiene mi entrega del proyecto de Pandas basada en el notebook del profesor `professor/pandas/09_limpieza_pandas_proyecto.ipynb`.

Contenido:
- `09_limpieza_pandas_proyecto.ipynb`: copia trabajada con ETL y EDA, incluyendo:
  - Carga robusta del dataset de Lending Club (`read_csv` con argumentos para resolver errores comunes).
  - Tabla `(column_name, type)` y conversión de tipos clave (fechas, porcentajes, categorías, etc.).
  - Manejo de NaNs/imputación con registro de estrategias en JSON.
  - Guardado/carga con Pickle del diccionario de datos (`LCDataDictionary.xlsx`).
  - Funciones de pipeline para reproducibilidad.

Cómo usar:
- Abre el notebook y ejecuta las celdas en orden.
- Requisitos: `pandas`, `numpy`.
- Nota: el notebook descarga datos desde URLs públicas; requiere internet para ejecutarse.

Entrega:
- Este trabajo está aislado en `students/luiscuellar31/pandas/` como solicita la guía.

