# Intro Python Interactivo — fundamentos y código «pythonic»

> Módulo práctico para aprender Python desde la acción: leer un poco, escribir mucho, medir y comparar enfoques. Pensado para principiantes, con énfasis en escribir código claro y «pythonic».

---

## ¿Qué es un Jupyter Notebook? (y cómo usarlo en VS Code)

Un cuaderno (Notebook) es un archivo interactivo con celdas de texto (Markdown) y celdas de código Python. Puedes ejecutar el código por partes y ver los resultados inmediatamente debajo de cada celda. Ideal para aprender y experimentar.

- Partes clave:
  - Celdas: bloques independientes (texto o código)
  - Kernel: el «motor» de Python que ejecuta las celdas (elige el intérprete correcto)
  - Botones de ejecución: ▶ para ejecutar una celda; Run All/Run Above para ejecutar varias

En VS Code, instala (si no los tienes):
- Extensión «Python» (ms-python.python)
- Extensión «Jupyter» (ms-toolsai.jupyter)
- Opcional: «Pylance» (tipos), «Black Formatter» (formato)

Flujo rápido en VS Code:
- Abre `notebooks/Intro_Python.ipynb`
- Selecciona kernel (arriba a la derecha): elige tu `.venv` si creaste uno
- Ejecuta celdas (botón ▶ a la izquierda de cada celda)
- Agrega una celda: usa el botón `+ Code` o `+ Markdown` (o el menú contextual en el borde de una celda)
- Convierte una celda: usa la barra superior de la celda (Code ↔ Markdown)
- Ejecuta todo: `Run All`, `Run Above`, `Run Below` (menú del cuaderno)
- Reinicia kernel: «Restart Kernel» si algo queda en un estado extraño

Sugerencia: modifica valores y re‑ejecuta. Aprenderás más experimentando.

---

## Objetivos

- Entender y practicar los tipos y estructuras básicas de Python.
- Escribir funciones pequeñas con docstrings y anotaciones de tipos.
- Usar patrones pythonic: comprensiones, `enumerate`, `zip`, desempaquetado, `with`.
- Medir tiempos con `timeit` para comparar enfoques (elegancia y rendimiento).
- Aprender de forma interactiva con un cuaderno (Jupyter/VS Code Notebook).

---

## Estructura de esta carpeta

```
professor/intro_python_interactivo/
  README.md                 ← esta guía
  requirements.txt          ← paquetes opcionales para notebook (ver abajo)
  notebooks/
    Intro_Python.ipynb      ← cuaderno interactivo con teoría mínima + ejercicios
  scripts/
    timing_basics.py        ← script CLI para medir tiempos de enfoques comunes
```

---

## Cómo usar (flujo sugerido)

1) Copia el material a tu carpeta de estudiante y trabaja SOLO ahí

```bash
mkdir -p students/{tu_usuario}/intro_python_interactivo
cp -r professor/intro_python_interactivo/* students/{tu_usuario}/intro_python_interactivo/
```

2) (Opcional pero recomendado) Crea un entorno virtual y activa

```bash
cd students/{tu_usuario}/intro_python_interactivo
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt || true  # todos los ejercicios funcionan sin extras
```

3) Abre el cuaderno y trabaja de forma interactiva

- En VS Code: abre `notebooks/Intro_Python.ipynb` y ejecuta celdas (íconos a la izquierda).
- O con Jupyter: `jupyter notebook` y navega al archivo.

4) Completa los TODOs en el cuaderno y corre los mini‑experimentos de tiempo

- En el cuaderno hay celdas para medir y comparar enfoques (`timeit`).
- También puedes usar el script CLI:

```bash
python scripts/timing_basics.py --help
python scripts/timing_basics.py --benchmark all --n 100000
```

5) (Opcional) Escribe un breve resumen de hallazgos

- ¿Qué enfoque fue más claro? ¿Cuál fue más rápido? ¿Cambió algo al variar `n`?

---

## Actividades clave en el cuaderno

- Variables y tipos (números, booleanos, cadenas, `None`).
- Colecciones (`list`, `tuple`, `set`, `dict`) y operaciones frecuentes.
- Verdad (truthiness), slicing y control de flujo.
- Funciones, docstrings, type hints, pruebas ligeras con `assert`.
- Patrones pythonic: comprensiones, `enumerate`, `zip`, desempacado, `with`.
- Errores/excepciones: `try/except`, `raise` con mensajes útiles.
- Módulos: importar y reutilizar.
- Medición de tiempo con `timeit` y diseño de pequeños experimentos.

Cada sección intercala teoría mínima con ejercicios prácticos y mini‑retos.

---

## Entrega sugerida (si aplica en tu curso)

Sube por Pull Request desde `students/{tu_usuario}/intro_python_interactivo/`:

- `notebooks/Intro_Python.ipynb` con los TODOs resueltos y celdas ejecutadas.
- (Opcional) `resultados_tiempos.txt` con 3–5 observaciones sobre rendimiento.

> Importante: no modifiques nada bajo `professor/`.

---

## Estilo y buenas prácticas

- Nombra en `snake_case`; funciones pequeñas que hagan una sola cosa.
- Prefiere claridad sobre «clever». Comenta solo lo no‑obvio.
- Usa f-strings para formatear: `f"x={x}"`.
- Apóyate en herramientas integradas: `sum`, `any`, `all`, `sorted`, `enumerate`.

Referencias útiles: PEP 8 (estilo), `help(obj)`, `dir(obj)`, `type(x)`.

---

## Comandos rápidos

```bash
# Abrir/activar entorno (opcional)
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt

# Ejecutar mediciones
python scripts/timing_basics.py --benchmark all --n 200000

# Abrir el cuaderno en VS Code
code notebooks/Intro_Python.ipynb
```

¡Listo! Abre el cuaderno, ejecuta, mide y reflexiona sobre el porqué de cada enfoque.
