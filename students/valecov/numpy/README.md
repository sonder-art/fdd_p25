# NumPy — Guía Interactiva y Progresiva

Aprenderás NumPy desde cero con cuadernos (Jupyter/VS Code Notebooks), pasando de conceptos básicos a prácticas de rendimiento y E/S con formatos comunes. El recorrido es incremental y autocontenido.

---

## Cómo estudiar este módulo

1) Copia este material a tu carpeta personal y trabaja SOLO ahí. No edites `professor/`.
2) Abre los notebooks en orden, ejecuta cada celda y modifica ejemplos.
3) Repite ejercicios clave hasta dominarlos sin ver solución.

```bash
mkdir -p students/{tu_usuario}/numpy
cp -r professor/numpy/* students/{tu_usuario}/numpy/

# (Opcional) Entorno virtual
cd students/{tu_usuario}/numpy
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt

# Registrar kernel de Jupyter para este entorno (opcional pero recomendado)
python -m ipykernel install --user --name numpy-venv --display-name "Python (numpy-venv)"
```

- En VS Code: selecciona el intérprete/Kernel "Python (numpy-venv)".
- En Jupyter clásico: al abrir el notebook, elige el Kernel "Python (numpy-venv)".

---

## Orden de notebooks (síguelos tal cual)

- `notebooks/01_Introduccion_NumPy.ipynb`
- `notebooks/02_Arrays_y_DTypes.ipynb`
- `notebooks/03_Slicing_Indexing_1D_2D.ipynb`
- `notebooks/04_Operaciones_Basicas_y_Broadcasting.ipynb`
- `notebooks/05_Reshape_Ejes_y_Agregaciones.ipynb`
- `notebooks/06_NaN_Inf_y_Tipos_Especiales.ipynb`
- `notebooks/07_Vectorizacion_vs_For_vs_Comprehensions.ipynb`
- `notebooks/08_IO_Pickle_JSON_NumPy.ipynb`
- `notebooks/09_Imagenes_RGB_y_Slicing_3D.ipynb`
- `notebooks/tarea_tiempos_numpy.ipynb`  # Tarea

> Nota: Varios cuadernos integran y mejoran el material de `legacy/` con más explicaciones y ejemplos.

---

## Qué practicarás

- Creación y propiedades de `ndarray`, `shape`, dtypes y casting
- Indexación y slicing en 1D/2D/3D; diferencias `n x 1` vs `n x None`
- Operaciones vectorizadas, broadcasting y comparaciones
- `reshape`, `axis`, agregaciones (`sum`, `mean`, etc.)
- Manejo de `NaN`, `Inf` y números especiales
- Medición de tiempos: vectorización vs bucles y comprensiones
- E/S con Pickle y JSON, serialización de tipos `numpy`
- Imágenes como arrays 3D y manipulación de canales RGB

---

## Requisitos

Instala dependencias mínimas si no abres los notebooks desde VS Code:

```bash
python -m pip install -r requirements.txt
```

### Alternativa rápida desde un notebook

En una celda del notebook, puedes instalar lo necesario (útil en entornos efímeros):

```python
!pip install numpy matplotlib ipykernel
```

Si quieres registrar el kernel de ese entorno directamente desde el notebook:

```python
import sys
!{sys.executable} -m ipykernel install --user --name numpy-venv --display-name "Python (numpy-venv)"
```

---

## Tarea: tiempos de ejecución con distintas estrategias

Propósito: practicar patrones de Python y contrastarlos con NumPy midiendo rendimiento.

Qué entregar (en `notebooks/tarea_tiempos_numpy.ipynb`):
- Tres problemas (P1 sencillo, P2 intermedio, P3 un poco más complejo).
- Para cada problema, cuatro versiones de la solución: for, list comprehension, generator (yield/expresión generadora) y NumPy vectorizado.
- Medición con `timeit` usando los mismos parámetros para todas las versiones. Reporta y comenta brevemente resultados.

Sugerencias:
- Verifica primero la corrección (formas/valores) entre versiones.
- Materializa el generador con `list(...)` al medir.
- Prueba tamaños `n` distintos para observar tendencias.

---

## Pedir ayuda

Cuando te atores, comparte el notebook, la celda y el error. Explica qué intentaste y tu hipótesis. Con eso te guiamos mejor.
