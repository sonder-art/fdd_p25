# Intro Python Interactivo — Guía de Autoestudio

Aprenderás Python de manera práctica y progresiva, escribiendo y ejecutando código en cuadernos interactivos (Jupyter/VS Code Notebooks). La idea es que avances de forma autodidacta siguiendo el orden propuesto, y que el profesor esté disponible para resolver dudas cuando las tengas.

---

## Qué es Python (en 30 segundos)

Python es un lenguaje de propósito general, con sintaxis legible y una curva de aprendizaje amable. Es interpretado y de tipado dinámico, ideal para aprender conceptos fundamentales de programación y para prototipar con rapidez. Aquí lo usarás para dominar las bases: tipos, colecciones, control de flujo, funciones, errores, y algunos patrones «pythonic».

---

## Cómo estudiar este módulo

1) Abre los notebooks y síguelos en el siguiente orden. Lee, ejecuta y modifica el código para comprobar tu comprensión. Tómate notas breves de lo que descubras.

2) Si te atoras, formula una duda concreta y consúltala con el profesor. La dinámica es autoestudio acompañado: tú avanzas, el profesor te desbloquea.

3) Repite: vuelve sobre ejercicios que cuesten hasta que te salgan de memoria sin mirar.

---

## Preparación: trabaja en tu carpeta de estudiante

Copia este material a tu carpeta personal y trabaja SOLO ahí. No edites nada bajo `professor/`.

```bash
mkdir -p students/{tu_usuario}/intro_python_interactivo
cp -r professor/intro_python_interactivo/* students/{tu_usuario}/intro_python_interactivo/

# (Opcional) Crea y activa un entorno virtual, e instala dependencias mínimas
cd students/{tu_usuario}/intro_python_interactivo
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
```

A partir de aquí, abre y trabaja los notebooks desde `students/{tu_usuario}/intro_python_interactivo/notebooks/`.

---

## Orden de notebooks (síguelos tal cual)

- `notebooks/01_Bienvenida_Jupyter.ipynb`
- `notebooks/02_Variables_y_Tipos.ipynb`
- `notebooks/03_Colecciones_y_Slicing.ipynb`
- `notebooks/04_Control_de_Flujo.ipynb`
- `notebooks/05a_Funciones_y_Docstrings.ipynb`
- `notebooks/05b_Alcance_y_Params_Avanzados.ipynb`
- `notebooks/06_Comprehensions_Map_Filter.ipynb`
- `notebooks/07_Errores_y_Excepciones.ipynb`
- `notebooks/08_Generadores_y_Yield.ipynb`
- `notebooks/09_Clases_y_Objetos_y_Proyecto.ipynb`

Nota: los cuadernos están numerados para marcar el recorrido recomendado. Avanza en orden, sin saltarte pasos.

---

## Cómo abrir y ejecutar los notebooks

- En VS Code: abre cualquier archivo `.ipynb` y ejecuta las celdas con el botón ▶ a la izquierda. Selecciona un kernel de Python válido (tu entorno actual) cuando VS Code lo solicite.
- Con Jupyter clásico: ejecuta `jupyter notebook` en la terminal y navega hasta el archivo.

Opcional (fuera de VS Code): instala las dependencias mínimas listadas en `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

---

## Qué practicarás

- Tipos y operaciones básicas
- Colecciones (`list`, `tuple`, `set`, `dict`) y slicing
- Control de flujo (`if/elif/else`, bucles)
- Funciones, docstrings y anotaciones de tipos
- Comprensiones, `enumerate`, `zip` y desempaquetado
- Manejo de errores con `try/except`
- Generadores y `yield`
- Clases y objetos (introducción) y un mini‑proyecto

Consejo: prioriza la claridad sobre lo rebuscado. Usa nombres descriptivos y prueba tus funciones con ejemplos pequeños.

---

## Pedir ayuda

Antes de preguntar, escribe lo que intentaste, el error observado y tu hipótesis. Con eso, el profesor podrá orientarte más rápido y mejor.

---

¡Listo! Abre el primer notebook y comienza. Ejecuta, explora y pregunta cuando lo necesites.
