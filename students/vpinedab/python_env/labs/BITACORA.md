# Bitácora — Mystery Lab (Docker + uv)

> **Alumno(a):** *Valentina Pineda*
---

## 1) Resumen ejecutivo

* **Objetivo:** Ejecutar `labs/mystery/main.py` en contenedor, descubriendo dependencias con **uv**, hasta obtener **exit code 0** y **tabla OK**.
* **Resultado:** **✓** Contenedor corre con **código 0** y muestra tabla con `uuid`.
* **Dependencias descubiertas:** `rich==13.7.1`, `httpx==0.27.2`.
* **Lecciones clave:**

  * `RUN source .venv/bin/activate` **no** persiste en capas de Docker; es mejor invocar el **intérprete del venv por ruta absoluta** en `CMD`.
  * **Instalar** con `uv` después de **COPY requirements.txt**.
  * Iterar por **ImportError/ModuleNotFoundError** hasta pasar a verde.

---

## 2) Selección de intérprete

* **Intérprete en contenedor:** `/app/.venv/bin/python3` (invocado directamente en `CMD`).
* **Evidencia (salida):**

```bash
which python3
python3 --version
pip --version
```

```bash
/usr/bin/python3
Python 3.12.3
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```
---

## 3) Estructura relevante

```text
students/vpinedab/python_env
├─ python.py
├─ requirements.txt
├─ README.md
└─ labs
  ├─ BITACORA.md 
  └─ mystery
    ├─ Dockerfile
    ├─ requirements.txt
    ├─ README.md
    └─ main.py                # (copiado en /app para este reto)
```

---

## 4) Bitácora técnica (Docker + uv)

### 4.1 Dockerfile — versión **inicial** (fallida)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY main.py .

RUN pip install uv
RUN uv venv .venv
RUN source .venv/bin/activate

RUN uv pip install -r requirements.txt

CMD ["python3", "main.py"]
```

**Problemas detectados:**

* `requirements.txt` estaba **vacío** y ni siquiera se copiaba, por eso no se instalaba nada.
* `RUN source .venv/bin/activate` **no** tiene efecto en la siguiente capa; `CMD ["python3", ...]` seguía usando el Python del sistema, **no** el del venv.
* En la primera corrida apareció: **`ModuleNotFoundError: No module named 'rich'`**.

---

### 4.2 Primera iteración — agregar `rich`

Acciones:

1. Validé con `pip list | grep "rich"` (para ver versión disponible); vi **`rich 13.7.1`**.
2. Añadí `rich==13.7.1` a `requirements.txt`.
3. Aun así fallaba porque el venv **no** estaba activándose realmente para `CMD`.

---

### 4.3 Ajuste crítico — usar el venv **por ruta** y copiar `requirements.txt`

**Decisión:** invocar el Python del venv directamente en `CMD` y copiar `requirements.txt` **antes** de instalar.

**Dockerfile — versión intermedia:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY main.py .
COPY requirements.txt .

RUN pip install uv
RUN uv venv .venv

RUN uv pip install -r requirements.txt

CMD ["/app/.venv/bin/python3", "main.py"]
```

Resultado: ahora sí usa `/app/.venv/bin/python3`. Apareció un nuevo error: **faltaba `httpx`**.

---

### 4.4 Segunda iteración — agregar `httpx`

* Intenté buscarlo con `pip list` (sin resultados útiles en ese momento).
* Añadí `httpx` “tal cual” → error por un problema del servidor/sobrecarga al resolver.
* **Solución:** fijar versión estable reciente: **`httpx==0.27.2`** en `requirements.txt`.
* Reconstruí y ejecuté: **OK**.

---

### 4.5 Dockerfile — versión **final**

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir uv
RUN uv venv .venv

# Instala dependencias del archivo (descubiertas por errores)
RUN uv pip install -r requirements.txt

# Importante: invocar el intérprete del venv por ruta absoluta
CMD ["/app/.venv/bin/python3", "main.py"]
```

---

## 5) `requirements.txt` final

```text
rich==13.7.1
httpx==0.27.2
```

---

## 6) Evidencia de ejecución

**Salida final observada:**

```
            Mystery App — Resultado             
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Clave ┃ Valor                                ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ uuid  │ 675885ea-2d08-4b2d-921d-0317af7ba0a1 │
└───────┴──────────────────────────────────────┘
OK — entorno configurado correctamente.
```
---

## 7) Tabla de iteraciones (errores → acciones)

| Iter | Error (extracto)                               | Causa raíz                             | Acción tomada                             | Resultado           |
| ---: | ---------------------------------------------- | -------------------------------------- | ----------------------------------------- | ------------------- |
|    1 | `ModuleNotFoundError: No module named 'rich'`  | No se instalaron deps; no COPY de reqs | `echo "rich==13.7.1" >> requirements.txt` | Fallo siguiente dep |
|    2 | Python seguía del sistema (no venv)            | `source` no persiste entre capas       | `CMD` → `"/app/.venv/bin/python3"`        | Avanza              |
|    3 | `ModuleNotFoundError: No module named 'httpx'` | Falta HTTP client                      | `echo "httpx" >> requirements.txt`        | Error servidor      |
|    4 | Falla al resolver/descargar `httpx`            | Servidor/sobrecarga                    | Fijar versión: `httpx==0.27.2`            | **OK**              |

---

## 8) Apéndice — Comandos usados

```bash
# build & run
docker build -t mystery-uv .
docker run --rm mystery-uv

# iterar deps
echo "rich==13.7.1" >> requirements.txt
echo "httpx==0.27.2" >> requirements.txt
docker build -t mystery-uv .
docker run --rm mystery-uv
```

---

## 9) Notas y aprendizajes

* En Docker, cada `RUN` crea una **capa**; `source` solo afecta a la **shell de esa capa**, no a las siguientes.
* La forma más robusta de usar el venv en `CMD` es **invocar su binario** por ruta absoluta.
* Colocar `COPY requirements.txt` **antes** de instalar permite cachear la capa y **reconstruir solo cuando cambian deps**.
* Para paquetes que fallan al resolverse, fijar una **versión conocida** suele estabilizar la build
