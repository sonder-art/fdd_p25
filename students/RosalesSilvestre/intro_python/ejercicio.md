

---

# 1) Qué debes entregar (lo único que revisaremos en tu PR)

En `students/{mi_carpeta}/intro_python/` deben estar estos **4 archivos**:

1. `notas.txt` — tus notas/resumen (lo irás llenando durante el ejercicio).
2. `entrega.py` — **lee `notas.txt` y lo imprime** por pantalla (si falta, error claro y salida ≠ 0).
3. `Dockerfile` — al ejecutar el contenedor, corre `python entrega.py`.
4. `README.md` — contiene **exactamente** estos dos comandos:

   ```bash
   docker build -t intro-python-entrega .
   docker run --rm intro-python-entrega
   ```

**Entrega:** por **Pull Request**.

---

# 2) Actualiza tu repo (recordatorio breve)

```bash
cd /ruta/a/tu/repo-clase
git fetch upstream
git checkout main
git merge upstream/main
# opcional:
# git push origin main
```

---

# 3) Copia el material base del profe a tu carpeta

```bash
mkdir -p students/{mi_carpeta}/intro_python
cp -r professor/intro_python/* students/{mi_carpeta}/intro_python/
ls -la students/{mi_carpeta}/intro_python
```

> Desde ahora, **trabaja SOLO** en `students/{mi_carpeta}/intro_python/`.

---

# 4) Verifica/instala Python 3

```bash
python3 -V || python -V
```

Si no tienes Python 3, instala y vuelve a probar:

**WSL2 Ubuntu/Debian/Linux Debian-like**

```bash
sudo apt update && sudo apt install -y python3 python3-pip
```

**macOS (Homebrew)**

```bash
brew install python
```

**Ahora abre `notas.txt` y completa la *Sección A*** (qué comando usarás: `python3` o `python`).

---

# 5) REPL (prueba guiada)


> **REPL (breve):** *Read–Eval–Print Loop* = Python lee → evalúa → imprime → espera. Úsalo para probar rápido; lo que quieras guardar va en archivos `.py`.  
Entra al REPL:

```bash
python3
```

Dentro, teclea **una por línea**:

```python
2 + 2
print("hola terminal")
import math; math.sqrt(144)
type(3.14)
help(len)  # para salir del help, pulsa q
```

Sal del REPL:

```python
exit()
```

**Abre `notas.txt` y completa la *Sección B*** (definición breve del REPL en tus palabras, 1–2 líneas).

---

# 6) Script mínimo `hola.py` (qué DEBE contener)

**Objetivo:** tu `hola.py` debe incluir **estos tres elementos** (tú lo codificas):

1. **Un `print()`** con un saludo o mensaje.
2. **Una variable** con el resultado de **una operación aritmética** y **un `print()`** mostrando ese resultado.
3. **Una función** muy simple y **un `print()`** mostrando la llamada a esa función con un valor.

Crea/edita y ejecuta:

```bash
nano hola.py       # escribe el script con esos 3 puntos; guarda y cierra
python3 hola.py    # ejecuta y observa la salida
```

**Abre `notas.txt` y completa la *Sección C*** (di qué contiene tu `hola.py` y resume qué viste al ejecutarlo).

---

# 7) Banderas de Python (ejecútalas y anota EXACTAMENTE lo pedido)

Ejecuta **cada** comando y **luego** anota en `notas.txt` (*Sección D*):

1. Ayuda general:

```bash
python3 -h
```

— En `-h:` escribe: “Mostró la ayuda general y las opciones de Python”.

2. Versión:

```bash
python3 -V
```

— En `-V:` escribe la versión exacta (ej.: “Python 3.12.x”).

3. Ejecutar una línea de código:

```bash
python3 -c "print('desde -c', 6*7)"
```

— En `-c:` escribe: “Ejecutó código pasado como texto y mostró la salida”.

4. Ejecutar script y quedarse en REPL con su estado:

```bash
python3 -i hola.py
# verás la salida; quedas en >>> ; sal con Ctrl+D
```

— En `-i:` escribe: “Ejecutó el script y me dejó en REPL con variables/funciones cargadas”.

5. Ejecutar módulos por nombre:

```bash
python3 -m this
python3 -m antigravity
```

— En `-m this:` y `-m antigravity:` describe **brevemente** qué ocurrió en cada uno.

---

# 8) `__pycache__`, `.pyc` (bytecode) y `dis`

1. Crea/observa `__pycache__`:

```bash
python3 hola.py
ls -la
ls -la __pycache__
```

— En `notas.txt` (*Sección E*): indica **cuándo aparece** y **qué hay dentro**.

2. Ver instrucciones con `dis`:

```bash
python3 -c "import dis, hola; dis.dis(hola)"
```

— En `notas.txt` (*Sección F*): escribe el comando que usaste y menciona que viste **instrucciones de bytecode** (nombra 1–2, p. ej. `LOAD_CONST`).

3. Banderas que afectan `.pyc`:

**`-B` (no escribir `.pyc`)**

```bash
rm -rf __pycache__
python3 -B hola.py
ls -la
```

— En *Sección E, `-B:`* escribe: “No se creó `__pycache__/` (no se escriben `.pyc`).”

**`-O` (optimización: elimina `assert`)**

```bash
rm -rf __pycache__
python3 -O hola.py
ls __pycache__
```

— En *Sección E, `-O:`* escribe: “Se crean `.pyc` optimizados; los `assert` no se evalúan.”

**`-OO` (más optimización: puede eliminar docstrings)**

```bash
rm -rf __pycache__
python3 -OO hola.py
ls __pycache__
```

— En *Sección E, `-OO:`* escribe: “`.pyc` optimizados; además pueden eliminarse docstrings.”

---

# 9) Entrega final (requisitos EXPLÍCITOS)

## 9.1 `entrega.py` (debe hacer EXACTAMENTE esto)

* **Abrir** `notas.txt` (mismo directorio).
* **Leer TODO** el contenido.
* **Imprimirlo TAL CUAL** (sin agregar ni quitar líneas).
* Si `notas.txt` **no existe**, **imprime un mensaje claro de error** y **termina con código ≠ 0**.

*(Pistas a investigar: `open`, `with`, `.read()`, `try/except FileNotFoundError`, `sys.exit(1)`.)*

Prueba:

```bash
python3 entrega.py
```

## 9.2 `Dockerfile` (debe lograr)

* Imagen base con **Python 3**.
* `WORKDIR` definido.
* `COPY` de `entrega.py` **y** `notas.txt` al contenedor.
* `CMD` que ejecute `python entrega.py`.

*(Pistas a investigar: `FROM`, `WORKDIR`, `COPY`, `CMD`.)*

## 9.3 `README.md` (contenido obligatorio)

Dentro, pega **exactamente**:

```bash
docker build -t intro-python-entrega .
docker run --rm intro-python-entrega
```

## 9.4 Verificación con Docker

```bash
docker build -t intro-python-entrega .
docker run --rm intro-python-entrega
```

— Debe imprimirse **exactamente** el contenido de `notas.txt`.

---

# 10) Sube y crea tu Pull Request

```bash
git add students/{mi_carpeta}/intro_python
git commit -m "Intro Python: notas.txt, entrega.py, Dockerfile y README"
git push origin <tu-rama>
```

Crea tu **PR** y verifica que están los 4 archivos.

