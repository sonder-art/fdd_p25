## Pandas Avanzado (15 minutos)



---

### 1) Joins y concatenaciones: `merge`, `join`, `concat`

- **Concepto clave**: un join es combinar filas de dos `DataFrame` alineando por claves (columnas o índices). El tipo de join controla qué filas se conservan.
  - **Inner**: intersección de claves.
  - **Left/Right**: conserva todas las filas del lado izquierdo/derecho.
  - **Outer**: unión de claves (rellena faltantes).
- **`merge`** (más flexible):
  - Por columnas con el mismo nombre: `pd.merge(df1, df2, on="id", how="left")`.
  - Con columnas con nombres distintos: `left_on="id_izq", right_on="id_der"`.
  - Por índice: `left_index=True`, `right_index=True`.
  - Útil: `indicator=True` para ver de dónde vino cada fila (`left_only`, `right_only`, `both`).
- **`join`** (atalajo por índice): `df1.join(df2, how="left")` asume índices; usa `on=` si `df2` debe unirse por columna en `df1`.
- **`concat`** (apila/pega):
  - Filas: `pd.concat([a, b], axis=0, ignore_index=True)`.
  - Columnas: `pd.concat([a, b], axis=1)` (alineación por índice).
  - Jerarquías: `keys=["a","b"]` crea un `MultiIndex` para rastrear el origen.
- **Índices e impacto**:
  - Asegura índices limpios/únicos si los usas como clave. `reset_index()` y `set_index()` son herramientas básicas.
  - Duplicados en claves → `merge` puede multiplicar filas (producto cartesiano por duplicados compartidos).

Ejemplo mínimo:

```python
pd.merge(df_ventas, df_clientes, on="cliente_id", how="outer", indicator=True)
```

---

### 2) Tiempo y fechas: `Timestamp`, `DatetimeIndex`, zonas horarias

- **`pd.Timestamp`**: instante en el tiempo. Puede ser "naive" (sin tz) o "aware" (con tz). Preferible trabajar en **UTC** y convertir al presentar.
- **Parseo**: `pd.to_datetime(col, utc=True, errors="coerce")` normaliza formatos y convierte a UTC.
- **Zonas horarias**:
  - Localizar naive: `.dt.tz_localize("America/Mexico_City")`.
  - Convertir tz: `.dt.tz_convert("UTC")`.
- **Índices temporales**: `DatetimeIndex` habilita slicing por fecha (`df['2023-05']`), `resample` (agregación por frecuencia: `"H"`, `"D"`, `"W"`, ...), y `asfreq`.
- **Granularidad**: comparar fechas con distinta granularidad (día vs minuto) requiere alinear (por ejemplo, truncar con `.dt.floor('D')`).
- **Combinar con tiempos**: `merge_asof` (joins por cercanía temporal) y `merge` normal si se igualan timestamps exactos.

Ejemplo mínimo:

```python
s = pd.to_datetime(pd.Series(["2024-01-01T10:00:00-06:00", "2024-01-01T10:05:00-06:00"]))
s_utc = s.dt.tz_convert("UTC")

df.resample("H").sum()  # agrega por hora
```

---

### 3) Tidy data: long vs wide con `melt`, `pivot`, `pivot_table`

- **Tidy data**: columnas = variables, filas = observaciones, celdas = valores.
- **`melt` (wide→long)**: especifica identificadores y columnas a derretir.
  - `pd.melt(df, id_vars=["id"], value_vars=["ene","feb"], var_name="mes", value_name="ventas")`.
- **`pivot` (long→wide)**: reestructura sin agregación. Requiere combinaciones únicas de `index` y `columns`.
  - `df.pivot(index="id", columns="mes", values="ventas")`.
- **`pivot_table`**: como `pivot` pero con agregación (maneja duplicados).
  - `df.pivot_table(index="id", columns="mes", values="ventas", aggfunc="sum")`.
- **`stack`/`unstack`**: reorganiza niveles de `MultiIndex` entre filas/columnas.

---

### 4) Limpieza end-to-end: valores faltantes, duplicados, tipos

- **Valores faltantes**: `isna`, `notna`, `fillna`, `dropna` (cuidado con `subset=` y `how=`).
- **Duplicados**: `duplicated`, `drop_duplicates` con `subset=` y `keep=`.
- **Tipos**: convertir con `astype`, `to_numeric(errors="coerce")`, `to_datetime(errors="coerce")`.
- **Textos/categorías**: `.str.strip().str.lower()`, `replace` (literal o regex), mapeos para homologar.
- **Outliers/reglas**: `clip`, validaciones con `between`, `where`, `mask`; chequeos con `assert` o contadores.
- **Un flujo típico**:
  1) Cargar datos sucios. 2) Normalizar tipos/fechas. 3) Homologar categorías. 4) Tratar nulos. 5) Deduplicar. 6) Validar. 7) Guardar limpio (CSV/Parquet).

Snippet útil:

```python
df["monto"] = pd.to_numeric(df["monto"], errors="coerce")
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", utc=True)
df = df.drop_duplicates(subset=["id"])  # deduplicación clave
```

---

### 5) EDA con pandas: `describe`, `value_counts`, `groupby`, `MultiIndex`

- **Exploración rápida**: `df.info()`, `df.describe(include="all")`, tipos, nulos.
- **Frecuencias**: `value_counts(normalize=True)`, `crosstab` (tablas de contingencia).
- **Agregaciones**: `groupby` con múltiples columnas, agregaciones nombradas:

```python
df.groupby(["categoria", "mes"]).agg(
    total=("monto", "sum"),
    promedio=("monto", "mean"),
    transacciones=("monto", "size"),
)
```

- **MultiIndex**: producido por `groupby` o `concat(keys=...)`; usar `reset_index()`, `unstack()` para reportes.
- **Pivotes**: `pivot_table` resume y reacomoda métricas para presentar.

---

### 6) Pipelines con `pipe` y SQL en pandas

- **`pipe`**: encadena transformaciones legibles aplicando funciones puras sobre `DataFrame`.

```python
def filtra_top(df):
    return df[df["monto"] > 0]

def agrega_flags(df):
    return df.assign(alto=df["monto"] > 1000)

resultado = (df
    .pipe(filtra_top)
    .pipe(agrega_flags)
)
```

- **SQL**: puedes usar `duckdb` para hacer SQL directamente sobre `DataFrame` de pandas:

```python
import duckdb
duckdb.query("SELECT categoria, SUM(monto) AS total FROM df GROUP BY 1").to_df()
```

- Patrón común: limpiar con pandas → enriquecer/estandarizar → consultas rápidas con SQL → reportes con `pivot_table`.

---

### Consejos prácticos

- Define llaves de join claramente y verifica duplicados antes de unir.
- Trabaja tiempos en UTC; convierte solo al mostrar.
- Estandariza categorías (case, espacios, sinónimos) antes de agrupar.
- Empieza EDA con conteos, nulos y distribuciones simples; luego profundiza con `groupby`.
- Encadena pasos con `pipe` para legibilidad y reusabilidad.

Sigue ahora los notebooks en `professor/pandas_v2/` en este orden sugerido:
1) 01_joins_indices.ipynb
2) 02_time_series_timestamps.ipynb
3) 03_tidy_data_melt_pivot.ipynb
4) 04_data_cleaning_flow.ipynb
5) 05_eda_groupby_multiindex.ipynb
6) 06_pipe_sql.ipynb

