# Implementación en Python: Del Modelo Matemático al Código

**Nota preliminar:** Este documento es una continuación directa de `README_v4.md`. Asumimos que el lector está familiarizado con los conceptos matemáticos formales presentados allí: tareas (τᵢ), conjuntos exec(τᵢ) y wait(τᵢ), concurrencia, asincronía, paralelismo, etc. Nuestro objetivo aquí es **conectar esos conceptos abstractos con código Python concreto**.

---

## 1. Introducción a las Herramientas de Python: Librería por Librería

En esta sección presentaremos las principales librerías de Python para implementar los modelos de ejecución estudiados. Cada librería ofrece herramientas específicas que mapean a diferentes propiedades matemáticas.

### 1.1 Visión General: Librería → Modelo

Antes de entrar en detalles, veamos qué librería se usa típicamente para cada modelo:

| Modelo (ver README_v4.md) | Librería principal | Componentes clave |
|---------------------------|-------------------|-------------------|
| **Secuencial** | (código Python estándar) | Funciones normales, sin concurrencia |
| **Asínc. no conc.** | `asyncio` | `async def`, `await` (sin `gather`) |
| **Conc. no asínc.** | `threading` | `Thread`, `Lock`, `Queue` |
| **Asínc. conc.** | `asyncio` | `async def`, `await`, `gather`, `create_task` |
| **Paralelo** | `concurrent.futures`, `multiprocessing` | `ProcessPoolExecutor`, `Process` |
| **Distribuido** | (librerías avanzadas) | `ray`, `dask`, `mpi4py` (no cubierto aquí) |

**Principio fundamental:** La misma propiedad matemática (ej: concurrencia) puede implementarse con diferentes mecanismos. Las librerías son **herramientas**, no los conceptos en sí.

---

### 1.2 Librería `asyncio`: Asincronía y Concurrencia sin Paralelismo

**Propósito:** Implementar ejecución **asíncrona y concurrente** en un solo hilo (P=1).

**Relación con el modelo:**
- Permite crear tareas τᵢ con wait(τᵢ) ≠ ∅ (asincronía)
- Permite solapamiento de vidas: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅ (concurrencia)
- Ejecuta en P=1 (sin paralelismo físico): ∀ t: |ExecutingAt(t)| ≤ 1

**Componentes principales:**

#### 1.2.1 `async def` - Definir una función asíncrona (corrutina)

**¿Qué es?** Una función declarada con `async def` es una **corrutina**: una función que puede pausarse y reanudarse.

**Relación con el modelo:**
- Una corrutina implementa una tarea τᵢ
- Puede tener periodos de ejecución exec(τᵢ) y espera wait(τᵢ)
- Al pausarse (con `await`), permite que otras corrutinas usen la CPU

**Ejemplo mínimo:**

```python
import asyncio

# Esto es una corrutina (función asíncrona)
async def tarea_simple():
    print("Inicio de la tarea")
    await asyncio.sleep(1)  # Simula una espera (wait)
    print("Fin de la tarea")
```

**Propiedades clave:**
- `async def` NO ejecuta nada por sí sola; solo **define** una corrutina
- Llamar `tarea_simple()` retorna un objeto coroutine, no ejecuta el código
- Necesitamos `await` o `asyncio.run()` para ejecutarla

**Error común (caso edge):**

```python
# ❌ INCORRECTO - esto NO ejecuta la tarea
tarea_simple()
# Retorna: <coroutine object tarea_simple at 0x...>
# ⚠️ Warning: coroutine 'tarea_simple' was never awaited
```

**¿Qué significa este error?** Llamar a `tarea_simple()` no ejecuta el código dentro de la función; solo crea un objeto "coroutine" (una promesa de ejecución futura). Es como escribir una receta en papel: la receta existe, pero nadie está cocinando. El warning te avisa que creaste una tarea que nunca se ejecutó porque nadie la "awaited" (esperó/ejecutó).

**Forma correcta:**

```python
# ✅ CORRECTO - ejecuta la corrutina
asyncio.run(tarea_simple())
# Imprime:
# Inicio de la tarea
# (espera 1 segundo)
# Fin de la tarea
```

**Analogía de cocina:**
- `async def` es la **receta** escrita en papel (no cocina nada por sí sola)
- `asyncio.run()` es el chef que **lee y ejecuta** la receta

---

#### 1.2.2 `await` - Pausar y esperar

**¿Qué es?** La palabra clave `await` **pausa** la corrutina actual hasta que la operación esperada complete.

**Relación con el modelo:**
- `await` marca el inicio de un periodo wait(τᵢ)
- Durante ese wait, el event loop puede ejecutar otras tareas (aprovechando la espera)
- Cuando la operación await termina, la corrutina reanuda (regresa a exec(τᵢ))

**Ejemplo mínimo:**

```python
import asyncio
from datetime import datetime

def tiempo():
    """Retorna timestamp legible: HH:MM:SS.mmm"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

async def tarea_con_espera():
    print(f"[{tiempo()}] Antes del await")
    await asyncio.sleep(2)  # Pausa aquí por 2 segundos
    print(f"[{tiempo()}] Después del await")

asyncio.run(tarea_con_espera())
# Imprime algo como:
# [14:23:10.234] Antes del await
# (espera 2 segundos - CPU disponible para otras tareas)
# [14:23:12.237] Después del await
#  ↑ Nota: ~2 segundos de diferencia
```

**Análisis temporal:**
- t=0: Imprime "Antes del await" (exec)
- t=0 a t=2: `await asyncio.sleep(2)` (wait) - CPU ociosa si no hay otras tareas
- t=2: Imprime "Después del await" (exec)

**Caso edge #1: `await` sin `async def`**

```python
# ❌ ERROR - await solo puede usarse dentro de async def
def funcion_normal():
    await asyncio.sleep(1)
# SyntaxError: 'await' outside async function
```

**Regla:** `await` **solo** puede usarse dentro de una función marcada con `async def`.

**Caso edge #2: `await` en código secuencial**

```python
import asyncio
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

async def tarea_a():
    print(f"[{tiempo()}] A inicio")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] A fin")

async def tarea_b():
    print(f"[{tiempo()}] B inicio")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] B fin")

# Ejecución secuencial (asíncrona NO concurrente)
async def main_secuencial():
    await tarea_a()  # Espera a que A termine completamente
    await tarea_b()  # Solo entonces inicia B

asyncio.run(main_secuencial())
# Imprime algo como:
# [14:30:00.100] A inicio
# (espera 1s)
# [14:30:01.102] A fin
# [14:30:01.102] B inicio  ← B inicia DESPUÉS de que A termine
# (espera 1s)
# [14:30:02.104] B fin
# Tiempo total: ~2 segundos
```

**¿Por qué `await tarea_a()` y no solo `tarea_a()`?**

Recordemos que `tarea_a()` es una función `async def`, por lo tanto llamarla **NO ejecuta su código**, solo crea un objeto coroutine:

```python
# ❌ INCORRECTO - no ejecuta nada
async def main_incorrecto():
    tarea_a()  # Solo crea la coroutine, no la ejecuta
    tarea_b()  # Solo crea la coroutine, no la ejecuta
    # ⚠️ Warning: coroutine 'tarea_a' was never awaited
    # ⚠️ Warning: coroutine 'tarea_b' was never awaited
    # NO se imprime nada

# ✅ CORRECTO - await ejecuta las corrutinas
async def main_correcto():
    await tarea_a()  # Ejecuta tarea_a completamente
    await tarea_b()  # Ejecuta tarea_b completamente
    # Imprime todo como esperamos
```

**Regla:** Dentro de una función `async def`, para ejecutar otra corrutina necesitas usar `await` (o pasarla a `gather`, `create_task`, etc.). Sin `await`, solo creas el objeto pero no lo ejecutas.

**Análisis del modelo:**
- ¿Hay asincronía? Sí: wait(tarea_a) ≠ ∅ y wait(tarea_b) ≠ ∅
- ¿Hay concurrencia? **NO**: [start(tarea_a), end(tarea_a)] ∩ [start(tarea_b), end(tarea_b)] = ∅
- **Modelo correspondiente:** Sección 3 (Asíncrono NO concurrente)
- La CPU está ociosa durante los `await` (no se aprovecha para ejecutar tarea_b)

**Analogía de cocina:**
- Chef inicia cafetera (tarea_a)
- Chef se queda mirando hasta que termine (await, CPU ociosa)
- Solo cuando termina la cafetera, inicia la tostadora (tarea_b)
- No aprovecha el tiempo de espera

**¿Por qué NO es concurrente si `await` libera recursos?**

Esta es una confusión muy común. Miremos el código línea por línea:

```python
async def main_secuencial():
    await tarea_a()  # ← LÍNEA 1: Se ejecuta primero
    await tarea_b()  # ← LÍNEA 2: No se ejecuta hasta que línea 1 complete
```

**El problema clave:**

Cuando ejecutas `await tarea_a()` en la LÍNEA 1, **pausas el flujo de ejecución de la corrutina `main_secuencial`**. Es decir, el "cursor" de ejecución de esa función **se queda detenido en la LÍNEA 1** y NO avanza a la LÍNEA 2 hasta que `await tarea_a()` complete.

**Importante:** `await` pausa **la corrutina actual** (main_secuencial), no solo "libera la CPU". El event loop puede ejecutar otras corrutinas, pero **dentro de main_secuencial**, el flujo de control está congelado en la línea del `await` y no puede avanzar a la siguiente línea hasta que termine.

**Visualización del flujo de control:**

```python
async def main_secuencial():
    await tarea_a()  # ← 👈 El "cursor" de main_secuencial se QUEDA AQUÍ
    await tarea_b()  # ← Esta línea NO SE LEE hasta que la anterior complete
```

**Timeline simplificado:**

```
t=0.0:  LÍNEA 1 ejecuta → await tarea_a() inicia tarea_a
        tarea_a imprime "A inicio" y entra en wait (sleep 1s)
        
        👉 Flujo de main_secuencial PAUSADO en LÍNEA 1
        ⚠️ LÍNEA 2 no se ha leído/ejecutado (el código no ha llegado ahí)
        ⚠️ tarea_b() nunca se llama, por lo tanto NO EXISTE
        ⚠️ Event loop libre, pero no hay otra tarea que ejecutar
        
t=1.0:  tarea_a completa → await tarea_a() retorna
        👉 Flujo de main_secuencial REANUDA y avanza a LÍNEA 2
        
t=1.0:  LÍNEA 2 ejecuta (recién ahora) → await tarea_b() inicia tarea_b
        tarea_b imprime "B inicio" y entra en wait
        👉 Flujo de main_secuencial PAUSADO en LÍNEA 2
        
t=2.0:  tarea_b completa → main_secuencial termina
```

**Analogía del flujo de control:** Es como leer un libro: cuando llegas a una nota que dice "ve a leer el Anexo A completo antes de continuar", dejas de leer esta página (pausas) y no lees la siguiente línea hasta que termines el Anexo A. El `await` es esa nota: "no sigas leyendo main_secuencial hasta que tarea_a() complete".

**Respuesta directa:** `await` libera el event loop SÍ, pero **la línea de código que llama a tarea_b() no se ejecuta** hasta que `await tarea_a()` complete. Sin esa línea ejecutándose, tarea_b nunca se crea.

**Para tener concurrencia necesitamos:** Llamar a ambas tareas **antes** de hacer await, para que existan simultáneamente. Eso lo veremos con `gather()` que hace algo como:

```python
# gather() internamente hace (simplificado):
tarea_obj_a = tarea_a()  # Crea tarea A (no la ejecuta aún)
tarea_obj_b = tarea_b()  # Crea tarea B (no la ejecuta aún)
# Ahora ambas EXISTEN simultáneamente
# Event loop las ejecuta intercaladamente aprovechando sus waits
```

---

#### 1.2.3 `asyncio.sleep()` - Simular espera asíncrona

**¿Qué es?** Pausa la corrutina actual por N segundos **sin bloquear el event loop**.

**Diferencia crucial con `time.sleep()`:**

```python
import time
import asyncio

# ❌ time.sleep() BLOQUEA todo el event loop
async def mal_ejemplo():
    print("Inicio")
    time.sleep(2)  # Bloquea completamente (ninguna otra tarea puede ejecutar)
    print("Fin")

# ✅ asyncio.sleep() permite que otras tareas ejecuten
async def buen_ejemplo():
    print("Inicio")
    await asyncio.sleep(2)  # Pausa esta tarea, otras pueden ejecutar
    print("Fin")
```

**Tabla comparativa:**

| Función | Bloquea event loop | Otras tareas pueden ejecutar | Modelo |
|---------|-------------------|------------------------------|--------|
| `time.sleep(n)` | ✅ Sí | ❌ No | Secuencial (bloquea todo) |
| `await asyncio.sleep(n)` | ❌ No | ✅ Sí | Asíncrono (libera CPU) |

**Regla de oro:** En código asíncrono, **NUNCA** uses `time.sleep()`. Siempre usa `await asyncio.sleep()`.

**Relación con el modelo:**
- `time.sleep(n)`: mantiene la CPU ocupada (simula exec(τᵢ) mal usado)
- `await asyncio.sleep(n)`: marca periodo wait(τᵢ), CPU disponible

**Nota práctica:**
En código real, `asyncio.sleep()` simula operaciones I/O como:
- `await fetch_url()` (descarga HTTP)
- `await read_file_async()` (lectura de disco)
- `await db_query()` (consulta a base de datos)

Todas estas operaciones tienen wait(τᵢ) ≠ ∅ porque esperan respuesta externa.

---

#### 1.2.4 `asyncio.gather()` - Ejecutar tareas concurrentemente

**¿Qué es?** Ejecuta múltiples corrutinas de forma **concurrente**, aprovechando los periodos wait de unas para ejecutar otras.

**Relación con el modelo:**
- Crea solapamiento de vidas de tareas (concurrencia)
- Implementa: ∃ i,j: exec(τⱼ) ∩ wait(τᵢ) ≠ ∅
- Modelo correspondiente: Sección 5 (Asíncrono y concurrente, sin paralelismo)

**Ejemplo mínimo:**

```python
import asyncio
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

async def tarea_a():
    print(f"[{tiempo()}] A inicio")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] A fin")
    return "Resultado A"

async def tarea_b():
    print(f"[{tiempo()}] B inicio")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] B fin")
    return "Resultado B"

# Ejecución concurrente
async def main_concurrente():
    print(f"[{tiempo()}] main_concurrente: antes de gather")
    resultados = await asyncio.gather(tarea_a(), tarea_b())
    print(f"[{tiempo()}] main_concurrente: después de gather")
    print(f"Resultados: {resultados}")

asyncio.run(main_concurrente())
# Imprime algo como:
# [14:45:00.100] main_concurrente: antes de gather
# [14:45:00.101] A inicio
# [14:45:00.101] B inicio
# (espera ~1s - ambas tareas en wait simultáneamente)
# [14:45:01.103] A fin
# [14:45:01.103] B fin
# [14:45:01.103] main_concurrente: después de gather
# Resultados: ['Resultado A', 'Resultado B']
# Tiempo total: ~1 segundo (no 2 como en el caso secuencial)
```

**Análisis temporal detallado:**

```
t=0.00: tarea_a inicia → print("A inicio")
t=0.00: tarea_a entra en wait (await asyncio.sleep(1))
t=0.00: event loop toma tarea_b (aprovecha wait de A)
t=0.00: tarea_b inicia → print("B inicio")
t=0.00: tarea_b entra en wait (await asyncio.sleep(1))
t=0.00-1.00: ambas en wait simultáneamente (CPU ociosa)
t=1.00: tarea_a despierta → print("A fin")
t=1.00: tarea_b despierta → print("B fin")
t=1.00: gather completa con resultados
```

**Propiedades clave:**
- ¿Hay solapamiento? Sí: ambas tareas viven de t=0 a t=1
- ¿Hay ejecución simultánea? **NO**: en cada instante, a lo más una ejecuta (|ExecutingAt(t)| ≤ 1)
- Mejora: tiempo total = max(tiempo_a, tiempo_b) ≈ 1s (vs 2s secuencial)

---

**Desglose: ¿Qué está pasando en cada parte del código?**

Analicemos la línea crítica:

```python
resultados = await asyncio.gather(tarea_a(), tarea_b())
```

**1. ¿Por qué `tarea_a()` y `tarea_b()` sin `await` directo?**

```python
# Cuando escribimos:
tarea_a()  # ← Crea el objeto coroutine (NO lo ejecuta)
tarea_b()  # ← Crea otro objeto coroutine (NO lo ejecuta)

# Ambos objetos coroutine EXISTEN simultáneamente
# Ahora se los pasamos a gather
```

**Clave:** Llamar a una función `async def` **sin await** solo crea el objeto coroutine, no lo ejecuta. Esto es exactamente lo que necesitamos: crear ambas tareas para que existan simultáneamente.

**2. ¿Qué hace `asyncio.gather()`?**

`gather()` toma múltiples coroutines y:
1. Las registra todas en el event loop
2. Las inicia (casi) simultáneamente
3. Retorna **una nueva coroutine** que espera a que todas completen
4. Cuando todas terminan, retorna una lista con sus resultados en orden

**3. ¿Por qué `await` antes de `gather()`?**

```python
# ❌ SIN await - no ejecuta nada
resultados = asyncio.gather(tarea_a(), tarea_b())
# resultados es un objeto coroutine, NO los resultados
# ⚠️ Warning: coroutine 'gather' was never awaited

# ✅ CON await - ejecuta las tareas
resultados = await asyncio.gather(tarea_a(), tarea_b())
# await ejecuta la coroutine que retorna gather
# resultados es ['Resultado A', 'Resultado B']
```

**Recordatorio:** `gather()` retorna una coroutine, y las coroutines necesitan `await` para ejecutarse.

**4. ¿Por qué necesitamos wrapear en `async def main_concurrente()` y usar `asyncio.run()`?**

**El problema:** `await` solo puede usarse dentro de funciones `async def`.

```python
# ❌ ESTO NO FUNCIONA - await en código top-level
import asyncio

resultados = await asyncio.gather(tarea_a(), tarea_b())
# SyntaxError: 'await' outside async function
```

**La solución:** Necesitamos dos pasos:

```python
# PASO 1: Wrapear en una función async
async def main_concurrente():
    resultados = await asyncio.gather(tarea_a(), tarea_b())
    # Aquí SÍ podemos usar await porque estamos en async def
    return resultados

# PASO 2: Iniciar el event loop con asyncio.run()
asyncio.run(main_concurrente())
# asyncio.run() crea el event loop y ejecuta main_concurrente
```

**¿Qué hace `asyncio.run()`?**
1. Crea un nuevo event loop
2. Ejecuta la coroutine que le pasas (main_concurrente)
3. Espera a que complete
4. Cierra el event loop
5. Retorna el resultado

**¿Qué es un event loop?**

El **event loop** es el "motor" que hace funcionar todo el sistema asíncrono. Es un bucle infinito que:

```python
# Pseudocódigo simplificado de cómo funciona un event loop
while hay_tareas_activas:
    # 1. Revisar qué tareas están listas para ejecutar
    tareas_listas = revisar_tareas_en_wait()  # ¿Ya terminó su sleep? ¿Llegó dato de red?
    
    # 2. Si hay tareas listas, ejecutar una
    if tareas_listas:
        tarea = seleccionar_tarea(tareas_listas)  # Típicamente FIFO
        ejecutar_hasta_proximo_await(tarea)       # Ejecuta hasta que haga await
    
    # 3. Si no hay tareas listas, esperar eventos
    else:
        esperar_evento_io()  # CPU ociosa hasta que algo despierte
```

**Responsabilidades del event loop:**
1. **Mantener registro de todas las tareas** (running, waiting, ready)
2. **Decidir qué tarea ejecutar** cuando una pausa (scheduler)
3. **Detectar cuándo una tarea en wait está lista** (I/O completado, timer expirado)
4. **Alternar entre tareas** para dar ilusión de concurrencia

**Analogía:** El event loop es como un jefe de cocina que:
- Mantiene lista de todas las órdenes activas
- Sabe qué chef está disponible y qué está esperando (cafetera, horno)
- Cuando una cafetera termina, le avisa al chef para que continúe
- Asigna al chef a otra orden mientras una está en espera

**En el contexto de `gather()`:**

Cuando ejecutamos `await asyncio.gather(tarea_a(), tarea_b())`:
1. gather registra tarea_a y tarea_b en el event loop
2. Event loop inicia tarea_a → ejecuta hasta su primer `await`
3. tarea_a hace `await asyncio.sleep(1)` → event loop la marca como "waiting"
4. Event loop toma tarea_b (porque tarea_a está en wait)
5. tarea_b ejecuta hasta su primer `await`
6. tarea_b hace `await asyncio.sleep(1)` → event loop la marca como "waiting"
7. Ambas en wait → event loop espera a que alguna despierte
8. Cuando una despierta, event loop la ejecuta hasta completar
9. gather retorna cuando ambas completaron

**Sin event loop:** No habría quien coordine las tareas, detecte cuándo están listas, ni las alterne. El event loop es el director de orquesta de todo el sistema asíncrono.

**Analogía completa:**
```python
asyncio.gather(tarea_a(), tarea_b())  # ← "Receta" para cocinar dos platos simultáneamente
await asyncio.gather(...)              # ← "Ejecutar" esa receta
async def main():                      # ← Envoltorio necesario (solo await vive en async def)
asyncio.run(main())                    # ← Iniciar la cocina (crear event loop)
```

**Resumen del flujo:**
```
1. tarea_a() → crea coroutine A (sin ejecutar)
2. tarea_b() → crea coroutine B (sin ejecutar)
3. gather(A, B) → crea coroutine que coordina A y B (sin ejecutar)
4. await gather(...) → ejecuta la coordinación (A y B corren concurrentemente)
5. asyncio.run() → crea el event loop que hace posible todo lo anterior
```

---

**Comparación: con gather vs sin gather**

```python
# Sin gather (secuencial)
async def sin_gather():
    await tarea_a()  # Termina en t=1
    await tarea_b()  # Termina en t=2
    # Tiempo total: 2 segundos

# Con gather (concurrente)
async def con_gather():
    await asyncio.gather(tarea_a(), tarea_b())
    # Tiempo total: 1 segundo (aprovecha waits)
```

**Caso edge: gather con tareas que no esperan**

```python
async def tarea_cpu_bound():
    resultado = sum(range(1000000))  # Trabajo intensivo, sin await
    return resultado

async def main():
    # gather no mejora nada aquí (no hay waits que aprovechar)
    await asyncio.gather(tarea_cpu_bound(), tarea_cpu_bound())
    # Tiempo: suma de ambas (ejecución secuencial efectiva)
```

**Lección:** `gather` solo da mejoras cuando las tareas tienen wait(τᵢ) ≠ ∅.

---

**Ejemplo avanzado: Trabajo CPU-bound antes del await**

Este ejemplo muestra cuándo exactamente el event loop puede cambiar entre tareas:

```python
import asyncio
import time
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def trabajo_pesado(duracion, nombre):
    """Simula trabajo CPU-bound (bloquea el event loop)"""
    print(f"[{tiempo()}] {nombre}: INICIO trabajo pesado ({duracion}s)")
    time.sleep(duracion)  # Simula cálculo pesado (bloquea)
    print(f"[{tiempo()}] {nombre}: FIN trabajo pesado")

async def tarea_con_trabajo_a():
    trabajo_pesado(0.5, "Tarea A")  # Trabajo ANTES del await
    print(f"[{tiempo()}] Tarea A: llegó al await")
    await asyncio.sleep(1)          # Ahora sí hace await
    print(f"[{tiempo()}] Tarea A: terminó el await")
    return "Resultado A"

async def tarea_con_trabajo_b():
    trabajo_pesado(0.3, "Tarea B")  # Trabajo ANTES del await
    print(f"[{tiempo()}] Tarea B: llegó al await")
    await asyncio.sleep(1)          # Ahora sí hace await
    print(f"[{tiempo()}] Tarea B: terminó el await")
    return "Resultado B"

async def main():
    print(f"[{tiempo()}] Main: antes de gather")
    resultados = await asyncio.gather(
        tarea_con_trabajo_a(),
        tarea_con_trabajo_b()
    )
    print(f"[{tiempo()}] Main: después de gather")
    print(f"Resultados: {resultados}")

asyncio.run(main())

# Imprime algo como:
# [15:30:00.100] Main: antes de gather
# [15:30:00.101] Tarea A: INICIO trabajo pesado (0.5s)
# [15:30:00.601] Tarea A: FIN trabajo pesado          ← 0.5s después
# [15:30:00.601] Tarea A: llegó al await               ← AQUÍ puede cambiar
# [15:30:00.601] Tarea B: INICIO trabajo pesado (0.3s) ← Ahora sí inicia B
# [15:30:00.901] Tarea B: FIN trabajo pesado          ← 0.3s después
# [15:30:00.901] Tarea B: llegó al await
# (ambas esperan ~1s)
# [15:30:01.602] Tarea A: terminó el await
# [15:30:01.902] Tarea B: terminó el await
# [15:30:01.902] Main: después de gather
# Resultados: ['Resultado A', 'Resultado B']
```

**Análisis temporal crítico:**

```
t=0.000: Main ejecuta gather → registra ambas tareas
t=0.001: Event loop inicia tarea_con_trabajo_a()
         ↓ Ejecuta trabajo_pesado(0.5s)
         ⚠️ Esta función NO es async, BLOQUEA el event loop
         ⚠️ tarea_con_trabajo_b() NO puede iniciar todavía
         
t=0.501: trabajo_pesado() termina
         Imprime "Tarea A: llegó al await"
         await asyncio.sleep(1) → Tarea A entra en WAIT
         👉 AHORA el event loop puede cambiar de tarea
         
t=0.501: Event loop toma tarea_con_trabajo_b() (recién ahora)
         ↓ Ejecuta trabajo_pesado(0.3s)
         ⚠️ Nuevamente bloquea el event loop
         
t=0.801: trabajo_pesado() termina
         Imprime "Tarea B: llegó al await"
         await asyncio.sleep(1) → Tarea B entra en WAIT
         
t=0.801-1.501: Ambas tareas en wait
t=1.501: Tarea A despierta
t=1.801: Tarea B despierta
```

**Observaciones clave:**

1. **No hay concurrencia en el trabajo pesado:** 
   - Tarea A ejecuta 0.5s de trabajo
   - Solo DESPUÉS Tarea B ejecuta 0.3s de trabajo
   - Total de trabajo CPU: 0.5s + 0.3s = 0.8s (secuencial)

2. **Sí hay concurrencia en los await:**
   - Ambas tareas esperan 1s simultáneamente
   - Se aprovecha el wait (como vimos antes)

3. **El event loop solo puede cambiar en await:**
   - Mientras ejecutas código síncrono (trabajo_pesado), el event loop está bloqueado
   - Solo cuando llegas a `await`, el event loop puede dar turno a otra tarea

4. **Tiempo total:** 0.5s (A trabaja) + 0.3s (B trabaja) + 1s (ambas esperan) ≈ 1.8s

**Comparación con trabajo pesado AL INICIO vs AL FINAL:**

```python
# Si el trabajo pesado estuviera DESPUÉS del await:
async def mejor_diseño():
    print(f"[{tiempo()}] Inicio")
    await asyncio.sleep(1)          # Primero hace await
    trabajo_pesado(0.5, "Trabajo")  # Luego hace trabajo
    print(f"[{tiempo()}] Fin")

# En este caso, AMBAS tareas podrían hacer await casi simultáneamente
# y el trabajo pesado se ejecutaría secuencialmente después
# (aunque seguiría sin haber mejora en el trabajo CPU)
```

**Lección crucial:** El event loop es **cooperativo**, no preemptive. Una tarea debe explícitamente ceder control con `await`. Si ejecutas código bloqueante (CPU-bound síncrono), TODO el event loop se bloquea hasta que termines y llegues al `await`.

**Regla de oro:** En código async, el trabajo pesado debe ir DESPUÉS de los await cuando sea posible, o mejor aún, usar `ProcessPoolExecutor` para trabajo CPU-bound (lo veremos en secciones posteriores).

---

**Analogía de cocina:**
- Sin gather: Chef inicia cafetera, se queda mirando hasta que termine, luego inicia tostadora
- Con gather: Chef inicia cafetera Y tostadora casi simultáneamente, aprovecha esperas de ambas

---

#### 1.2.5 `asyncio.create_task()` - Lanzar tarea sin esperar inmediatamente

**Problema que resuelve:**

Hasta ahora hemos visto dos enfoques:
1. `await tarea()` - Inicia tarea y ESPERA hasta que termine antes de continuar
2. `await gather(tarea_a(), tarea_b())` - Inicia ambas y ESPERA hasta que ambas terminen

Pero, ¿qué pasa si quiero:
- Iniciar una tarea
- Seguir haciendo otras cosas en mi código
- Y LUEGO, cuando sea necesario, esperar su resultado?

**Aquí entra `create_task()`:** Lanza una tarea para que corra "en background" mientras tú continúas con tu código.

---

**Comparación visual: Los tres enfoques**

```python
# ENFOQUE 1: await directo (bloquea hasta terminar)
async def enfoque_1():
    print("Antes")
    await tarea_larga()  # ← Código se DETIENE aquí hasta que termine
    print("Después")     # ← Esta línea NO se ejecuta hasta que tarea_larga() termine

# ENFOQUE 2: gather (inicia múltiples, espera a todas)
async def enfoque_2():
    print("Antes")
    await gather(tarea_a(), tarea_b())  # ← Detiene aquí hasta que AMBAS terminen
    print("Después")                    # ← NO se ejecuta hasta que ambas terminen

# ENFOQUE 3: create_task (inicia y continúa, espera después)
async def enfoque_3():
    print("Antes")
    task = create_task(tarea_larga())  # ← Lanza tarea pero NO espera
    print("Durante")                    # ← Esta línea SÍ se ejecuta inmediatamente
    # ... hacer otras cosas mientras tarea_larga() corre en background ...
    resultado = await task              # ← AQUÍ esperamos cuando necesitamos el resultado
    print("Después")
```

**Diferencia clave:** Con `create_task()`, el flujo de tu función `main` NO se pausa inmediatamente. Puedes seguir ejecutando código mientras la tarea corre en paralelo (concurrentemente).

---

**Ejemplo con timestamps (el contraste es crucial):**

```python
import asyncio
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

async def tarea_larga():
    print(f"[{tiempo()}] Tarea larga: INICIO")
    await asyncio.sleep(2)
    print(f"[{tiempo()}] Tarea larga: FIN")
    return "Resultado de tarea larga"

# VERSIÓN A: Con await directo (bloquea)
async def version_await_directo():
    print(f"[{tiempo()}] Main: inicio")
    
    await tarea_larga()  # ← Se DETIENE aquí
    
    # ⚠️ Esta línea NO se ejecuta hasta que tarea_larga() termine (2s después)
    print(f"[{tiempo()}] Main: después de tarea_larga")
    print(f"[{tiempo()}] Main: haciendo otra cosa")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] Main: fin")

asyncio.run(version_await_directo())
# Salida:
# [16:00:00.100] Main: inicio
# [16:00:00.101] Tarea larga: INICIO
# (espera 2s - main está PAUSADO)
# [16:00:02.102] Tarea larga: FIN
# [16:00:02.102] Main: después de tarea_larga    ← Recién ahora ejecuta esto
# [16:00:02.102] Main: haciendo otra cosa
# (espera 1s)
# [16:00:03.103] Main: fin
# Tiempo total: 3s (2s + 1s secuencial)


# VERSIÓN B: Con create_task (NO bloquea)
async def version_create_task():
    print(f"[{tiempo()}] Main: inicio")
    
    task = asyncio.create_task(tarea_larga())  # ← Lanza pero NO espera
    
    # ✅ Esta línea SÍ se ejecuta inmediatamente
    print(f"[{tiempo()}] Main: después de create_task (tarea en background)")
    print(f"[{tiempo()}] Main: haciendo otra cosa")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] Main: terminé mi trabajo")
    
    # Ahora sí esperamos el resultado
    print(f"[{tiempo()}] Main: esperando resultado de task")
    resultado = await task
    print(f"[{tiempo()}] Main: fin - resultado: {resultado}")

asyncio.run(version_create_task())
# Salida:
# [16:00:00.100] Main: inicio
# [16:00:00.101] Main: después de create_task (tarea en background)
# [16:00:00.101] Main: haciendo otra cosa
# [16:00:00.101] Tarea larga: INICIO              ← Inicia casi simultáneamente
# (ambas esperan - main 1s, tarea_larga 2s)
# [16:00:01.102] Main: terminé mi trabajo         ← Main despierta primero
# [16:00:01.102] Main: esperando resultado de task
# (main espera 1s más a que tarea_larga termine)
# [16:00:02.102] Tarea larga: FIN
# [16:00:02.102] Main: fin - resultado: Resultado de tarea larga
# Tiempo total: 2s (máximo de ambas, no suma)
```

**Análisis detallado con timestamps:**

**VERSIÓN A (await directo):**
```
t=0.000: Main inicio
t=0.001: await tarea_larga() → PAUSA main aquí
t=0.001: Tarea larga INICIO
t=0.001-2.002: Tarea larga en wait (main PAUSADO esperando)
t=2.002: Tarea larga FIN
t=2.002: Main REANUDA y continúa con la siguiente línea
t=2.002: Main imprime "después de tarea_larga"
t=2.002: Main imprime "haciendo otra cosa"
t=2.002-3.003: Main en wait (sleep 1s)
t=3.003: Main fin
Tiempo total: 3s
```

**VERSIÓN B (create_task):**
```
t=0.000: Main inicio
t=0.001: create_task(tarea_larga()) → Registra tarea pero NO pausa main
t=0.001: Main imprime "después de create_task" (inmediatamente)
t=0.001: Main imprime "haciendo otra cosa" (inmediatamente)
t=0.001: Event loop inicia tarea_larga en background
t=0.001: Tarea larga INICIO
t=0.001: Main hace await asyncio.sleep(1)
t=0.001-1.002: Ambas en wait (main 1s, tarea_larga 2s en paralelo)
t=1.002: Main despierta
t=1.002: Main imprime "terminé mi trabajo"
t=1.002: Main hace await task (espera a tarea_larga)
t=1.002-2.002: Main esperando a que tarea_larga termine (1s más)
t=2.002: Tarea larga FIN
t=2.002: Main obtiene resultado
t=2.002: Main fin
Tiempo total: 2s (¡1 segundo menos!)
```

**Diferencia clave:**
- **Con await directo:** Main se DETIENE en `await tarea_larga()` y no puede ejecutar "haciendo otra cosa" hasta que termine (2s después)
- **Con create_task:** Main CONTINÚA inmediatamente después de `create_task()`, ejecuta "haciendo otra cosa" (sleep 1s) **mientras** tarea_larga corre en background (2s). Resultado: overlapping time.

---

**¿Cuándo usar cada enfoque?**

**Usa `await directo` cuando:**
```python
# Necesitas el resultado INMEDIATAMENTE para continuar
async def ejemplo():
    usuario = await obtener_usuario(id=123)
    # ↓ Necesito 'usuario' aquí para la siguiente línea
    permisos = await obtener_permisos(usuario.rol)
```

**Usa `gather()` cuando:**
```python
# Tienes múltiples tareas independientes y necesitas todos los resultados
async def ejemplo():
    resultados = await asyncio.gather(
        descargar_url("https://a.com"),
        descargar_url("https://b.com"),
        descargar_url("https://c.com")
    )
    # Necesito los 3 resultados al mismo tiempo para procesarlos
```

**Usa `create_task()` cuando:**
```python
# Quieres iniciar algo temprano pero no necesitas el resultado todavía
async def ejemplo():
    # Inicio descarga pesada temprano
    task_descarga = asyncio.create_task(descargar_archivo_grande())
    
    # Mientras tanto, hago validaciones rápidas
    validar_permisos()
    preparar_directorio()
    
    # AHORA sí necesito el archivo
    archivo = await task_descarga
    procesar(archivo)
```

**Otro ejemplo práctico:**
```python
# Caso real: web scraper
async def scrape_sitio():
    # Inicio página principal (tarda 2s)
    task_main = create_task(descargar_pagina_principal())
    
    # Mientras tanto, descargo CSS/JS (tarda 1s cada uno)
    css = await descargar_css()
    js = await descargar_js()
    
    # Ahora sí espero la página principal
    html = await task_main
    
    # Proceso: CSS+JS tomaron 2s, página tomó 2s, pero se overlapearon
    # Tiempo total: 2s (no 4s)
```

---

**Caso edge: Olvidar el await final**

```python
async def error_comun():
    task = asyncio.create_task(tarea_importante())
    
    # ❌ Olvido hacer await task
    print("Main termina")
    # ⚠️ Warning: Task was destroyed but it is pending!
    # La tarea puede cancelarse si main termina primero

# ✅ CORRECTO: Siempre hacer await al final
async def correcto():
    task = asyncio.create_task(tarea_importante())
    # ... hacer otras cosas ...
    await task  # ← Importante: esperar antes de terminar
```

---

**Comparación final: Los tres enfoques lado a lado**

```python
import asyncio
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

async def tarea_a():
    print(f"[{tiempo()}] A inicio")
    await asyncio.sleep(2)
    print(f"[{tiempo()}] A fin")
    return "A"

async def tarea_b():
    print(f"[{tiempo()}] B inicio")
    await asyncio.sleep(1)
    print(f"[{tiempo()}] B fin")
    return "B"

# OPCIÓN 1: await directo (secuencial)
async def opcion_1():
    print(f"[{tiempo()}] === OPCIÓN 1: await directo ===")
    a = await tarea_a()  # Espera 2s
    b = await tarea_b()  # Espera 1s más
    print(f"Resultados: {a}, {b}")
    # Tiempo: 3s (2s + 1s)

# OPCIÓN 2: gather (concurrente, espera a ambas)
async def opcion_2():
    print(f"[{tiempo()}] === OPCIÓN 2: gather ===")
    resultados = await asyncio.gather(tarea_a(), tarea_b())
    print(f"Resultados: {resultados}")
    # Tiempo: 2s (máximo de ambas)

# OPCIÓN 3: create_task (concurrente, control fino)
async def opcion_3():
    print(f"[{tiempo()}] === OPCIÓN 3: create_task ===")
    task_a = asyncio.create_task(tarea_a())
    task_b = asyncio.create_task(tarea_b())
    
    print(f"[{tiempo()}] Tareas lanzadas, haciendo otra cosa...")
    await asyncio.sleep(0.5)  # Simulamos trabajo
    print(f"[{tiempo()}] Terminé mi trabajo, esperando resultados...")
    
    a = await task_a
    b = await task_b
    print(f"Resultados: {a}, {b}")
    # Tiempo: 2s (máximo de ambas, igual que gather)
    # PERO pudimos hacer trabajo adicional mientras esperaban

# Ejecutar cada opción
asyncio.run(opcion_1())
# [16:00:00.100] === OPCIÓN 1: await directo ===
# [16:00:00.101] A inicio
# [16:00:02.102] A fin
# [16:00:02.102] B inicio
# [16:00:03.103] B fin
# Resultados: A, B
# Tiempo: 3s

asyncio.run(opcion_2())
# [16:00:03.200] === OPCIÓN 2: gather ===
# [16:00:03.201] A inicio
# [16:00:03.201] B inicio
# [16:00:05.202] A fin
# [16:00:04.202] B fin
# Resultados: ['A', 'B']
# Tiempo: 2s

asyncio.run(opcion_3())
# [16:00:05.300] === OPCIÓN 3: create_task ===
# [16:00:05.301] Tareas lanzadas, haciendo otra cosa...
# [16:00:05.301] A inicio
# [16:00:05.301] B inicio
# [16:00:05.801] Terminé mi trabajo, esperando resultados...
# [16:00:06.302] B fin
# [16:00:07.302] A fin
# Resultados: A, B
# Tiempo: 2s (pero con trabajo extra en el medio)
```

---

**Resumen visual:**

```
await directo:        [ESPERA A]----[ESPERA B]----  (secuencial)
                      
gather:               [ESPERA A y B simultáneas]----  (espera desde inicio)
                      
create_task:          [LANZA A y B]--[HACE OTRAS COSAS]--[ESPERA resultados]
                                     ↑
                                     Diferencia clave: puedes trabajar aquí
```

**Analogía de cocina final:**
- **await directo:** Chef inicia cafetera, se queda mirando 5min, luego inicia tostadora, se queda mirando 2min. (7min total)
- **gather:** Chef inicia cafetera Y tostadora simultáneamente, se queda mirando ambas hasta que terminen. (5min total)
- **create_task:** Chef inicia cafetera Y tostadora, **mientras tanto corta fruta**, luego verifica que cafetera y tostadora hayan terminado. (5min total + fruta cortada)

---

#### 1.2.6 `asyncio.wait()` - Control avanzado sobre múltiples tareas

**¿Qué es?** Similar a `gather`, pero con más control: puedes esperar hasta que termine la primera, o un subconjunto, etc.

**Diferencia con `gather`:**
- `gather`: espera a que **todas** terminen, retorna lista de resultados en orden
- `wait`: puedes esperar a que **algunas** terminen (primera, todas, o hasta timeout)

**Ejemplo mínimo:**

```python
import asyncio

async def tarea(nombre, duracion):
    print(f"{nombre} inicio")
    await asyncio.sleep(duracion)
    print(f"{nombre} fin")
    return f"Resultado {nombre}"

async def main():
    # Crear tareas
    task_a = asyncio.create_task(tarea("A", 1))
    task_b = asyncio.create_task(tarea("B", 2))
    task_c = asyncio.create_task(tarea("C", 3))
    
    # Esperar hasta que la primera termine
    done, pending = await asyncio.wait(
        {task_a, task_b, task_c},
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"Primera tarea completada: {done}")
    print(f"Tareas pendientes: {pending}")
    
    # Cancelar las pendientes
    for task in pending:
        task.cancel()

asyncio.run(main())
# Imprime:
# A inicio
# B inicio
# C inicio
# (espera ~1s)
# A fin
# Primera tarea completada: {<Task task_a>}
# Tareas pendientes: {<Task task_b>, <Task task_c>}
```

**Opciones de `return_when`:**

```python
# 1. FIRST_COMPLETED - retorna cuando la primera termine
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

# 2. FIRST_EXCEPTION - retorna cuando una falle
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

# 3. ALL_COMPLETED - retorna cuando todas terminen (similar a gather)
done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
```

**Caso edge: wait sin await**

```python
# ❌ ERROR - wait retorna una corrutina que debe ser awaited
async def main_incorrecto():
    tasks = [asyncio.create_task(tarea("A", 1))]
    done, pending = asyncio.wait(tasks)  # Falta await
    # TypeError: cannot unpack non-iterable coroutine object
```

**Correcto:**

```python
async def main_correcto():
    tasks = [asyncio.create_task(tarea("A", 1))]
    done, pending = await asyncio.wait(tasks)  # ✅ Con await
```

**¿Cuándo usar wait vs gather?**

| Situación | Usar |
|-----------|------|
| Quieres todos los resultados en orden | `gather` |
| Quieres procesar resultados conforme llegan | `wait` con `FIRST_COMPLETED` |
| Necesitas timeout o cancelación | `wait` con `timeout` |
| Código simple sin casos especiales | `gather` |

**Analogía de cocina:**
- `gather`: Chef espera a que cafetera, tostadora y licuadora terminen
- `wait(FIRST_COMPLETED)`: Chef espera a que **cualquiera** termine para actuar (atiende la primera alarma)

---

#### 1.2.7 Event Loop - El corazón de asyncio

**¿Qué es?** El **event loop** es el scheduler que gestiona la ejecución de corrutinas, decidiendo cuál ejecutar en cada momento.

**Relación con el modelo:**
- Event loop implementa el planificador (scheduler) mencionado en el modelo matemático
- Mantiene cola de tareas listas (ready queue)
- Cuando una tarea hace `await`, el loop selecciona otra tarea lista

**Funcionamiento interno simplificado:**

```
while hay_tareas_activas:
    1. Revisar si alguna tarea en wait ya puede continuar (I/O completado, timer expirado)
    2. Mover esas tareas a la cola de listas (ready queue)
    3. Si hay tareas listas:
       a. Seleccionar una tarea (típicamente FIFO)
       b. Ejecutarla hasta el próximo await
       c. Si hace await, moverla a wait y repetir
    4. Si no hay tareas listas, esperar evento I/O (CPU ociosa)
```

**Ejemplo explícito del event loop:**

```python
import asyncio

async def tarea(nombre):
    print(f"{nombre} - inicio")
    await asyncio.sleep(0)  # Yield control al event loop
    print(f"{nombre} - después de primer yield")
    await asyncio.sleep(0)  # Yield control nuevamente
    print(f"{nombre} - fin")

async def main():
    await asyncio.gather(tarea("A"), tarea("B"))

asyncio.run(main())
# Imprime:
# A - inicio
# B - inicio
# A - después de primer yield
# B - después de primer yield
# A - fin
# B - fin
```

**Análisis de scheduling:**

```
t=0: Event loop inicia tarea A
     → print("A - inicio")
     → await asyncio.sleep(0) [A entra en wait]
     → Event loop cambia a tarea B

t=1: Event loop ejecuta tarea B
     → print("B - inicio")
     → await asyncio.sleep(0) [B entra en wait]
     → Event loop vuelve a A (ambas listas)

t=2: Event loop ejecuta tarea A
     → print("A - después de primer yield")
     → await asyncio.sleep(0) [A entra en wait]
     → Event loop cambia a B

t=3: Event loop ejecuta tarea B
     → print("B - después de primer yield")
     → await asyncio.sleep(0) [B entra en wait]
     → Event loop vuelve a A

t=4: A y B completan
```

**Propiedad clave:** El event loop es **cooperativo** (no preemptive):
- Una tarea solo cede control cuando hace `await`
- Si una tarea ejecuta código bloqueante (ej: `time.sleep`), **bloquea todo el event loop**

**Caso edge: bloquear el event loop**

```python
import asyncio
import time

async def tarea_mala():
    print("Inicio tarea mala")
    time.sleep(5)  # ❌ Bloquea TODO el event loop por 5s
    print("Fin tarea mala")

async def tarea_buena():
    print("Inicio tarea buena")
    # Esta no puede ejecutar mientras tarea_mala bloquea
    await asyncio.sleep(1)
    print("Fin tarea buena")

async def main():
    await asyncio.gather(tarea_mala(), tarea_buena())
    # tarea_buena NO puede ejecutar hasta que tarea_mala termine

asyncio.run(main())
# Tiempo total: ~5s (no concurrencia efectiva)
```

**Regla de oro:** Nunca bloquees el event loop con operaciones síncronas largas.

**Acceso explícito al event loop:**

```python
import asyncio

async def main():
    # Obtener referencia al event loop actual
    loop = asyncio.get_event_loop()
    
    # O en Python 3.10+
    loop = asyncio.get_running_loop()
    
    # Usar el loop para scheduling avanzado
    loop.call_later(2.0, lambda: print("Callback después de 2s"))
    
    await asyncio.sleep(3)

asyncio.run(main())
```

**Analogía de cocina:**
- Event loop = Jefe de cocina que decide qué orden atiende el chef
- Ready queue = Lista de órdenes listas para trabajar
- Wait state = Órdenes esperando dispositivos (cafetera, horno)
- `await` = Chef reporta "estoy esperando la cafetera" y jefe asigna otra orden

---

### 1.3 Librería `threading`: Concurrencia sin Asincronía (Time-slicing)

**Propósito:** Implementar concurrencia mediante **múltiples hilos del OS** con time-slicing.

**Relación con el modelo:**
- Permite solapamiento de vidas de tareas (concurrencia)
- Típicamente sin esperas reales (wait(τᵢ) = ∅), o con waits bloqueantes
- En Python: limitado por GIL (Global Interpreter Lock) → típicamente P=1 efectivo
- Modelo correspondiente: Sección 4 (Concurrente NO asíncrono, sin paralelismo)

**Componentes principales:**

#### 1.3.1 `threading.Thread` - Crear un hilo

**¿Qué es?** Representa un hilo del sistema operativo que ejecuta código de forma concurrente.

**Ejemplo mínimo:**

```python
import threading
import time
import os
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def tarea(nombre, duracion):
    print(f"[{tiempo()}] {nombre} - inicio (Hilo: {threading.current_thread().name})")
    time.sleep(duracion)  # Simula trabajo (aquí bloqueante está OK para I/O)
    print(f"[{tiempo()}] {nombre} - fin")

# Información del sistema
print(f"Cores disponibles: {os.cpu_count()}")
print(f"[{tiempo()}] Main: creando hilos...")

# Crear hilos
hilo_a = threading.Thread(target=tarea, args=("A", 2), name="Thread-A")
hilo_b = threading.Thread(target=tarea, args=("B", 1), name="Thread-B")

# Iniciar hilos
print(f"[{tiempo()}] Main: iniciando hilos...")
hilo_a.start()
hilo_b.start()

# Esperar a que terminen
hilo_a.join()
hilo_b.join()

print(f"[{tiempo()}] Main: todos los hilos terminaron")

# Imprime algo como:
# Cores disponibles: 8
# [17:00:00.100] Main: creando hilos...
# [17:00:00.101] Main: iniciando hilos...
# [17:00:00.102] A - inicio (Hilo: Thread-A)
# [17:00:00.102] B - inicio (Hilo: Thread-B)
# (después de ~1s)
# [17:00:01.103] B - fin
# (después de ~1s más)
# [17:00:02.103] A - fin
# [17:00:02.103] Main: todos los hilos terminaron
```

**Análisis temporal:**

```
Sistema: 8 cores disponibles

t=0.100: Main crea hilos
t=0.101: Main inicia hilos (start())
t=0.102: OS scheduler asigna Thread-A a ejecutar
t=0.102: Thread-A imprime "A - inicio"
t=0.102: Thread-A hace time.sleep(2) → libera GIL
         ↓
         OS puede cambiar de thread
         ↓
t=0.102: OS scheduler asigna Thread-B a ejecutar
t=0.102: Thread-B imprime "B - inicio"
t=0.102: Thread-B hace time.sleep(1) → libera GIL
         ↓
         Ambos threads en espera I/O (sleep)
         ↓
t=1.103: Thread-B despierta (sleep 1s completado)
t=1.103: Thread-B imprime "B - fin" y termina
t=2.103: Thread-A despierta (sleep 2s completado)
t=2.103: Thread-A imprime "A - fin" y termina
t=2.103: Main continúa después de join()

Tiempo total: ~2s (máximo de ambos, no suma)
```

---

**¿Estamos usando múltiples cores o un solo core?**

Esta es una pregunta crucial. La respuesta depende del **tipo de trabajo**:

**En este ejemplo (time.sleep - I/O simulado):**
- **Respuesta corta:** Técnicamente podría usar múltiples cores, pero NO IMPORTA porque ambos hilos están en ESPERA (sleep), no ejecutando.
- Durante `time.sleep()`, el hilo libera el GIL y el sistema operativo puede programar otros hilos
- Como ambos hilos pasan la mayoría del tiempo en sleep (I/O wait), no compiten por CPU
- **Tiempo total: ~2s** (se aprovechan las esperas)

**Si fuera trabajo CPU-bound (cálculos intensivos):**

Agreguemos un ejemplo para ver la diferencia:

```python
import threading
import time
import os
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def tarea_cpu_intensiva(nombre):
    """Trabajo CPU-bound: cálculos sin I/O"""
    print(f"[{tiempo()}] {nombre} - inicio")
    resultado = sum(range(20_000_000))  # Cálculo puro, sin sleep
    print(f"[{tiempo()}] {nombre} - fin (resultado: {resultado})")

print(f"Cores disponibles: {os.cpu_count()}")

# PRUEBA 1: Con threading (GIL limita a 1 core efectivo)
print(f"\n=== CON THREADING (múltiples hilos, 1 core efectivo) ===")
inicio = time.time()
hilo_a = threading.Thread(target=tarea_cpu_intensiva, args=("Thread-A",))
hilo_b = threading.Thread(target=tarea_cpu_intensiva, args=("Thread-B",))
hilo_a.start()
hilo_b.start()
hilo_a.join()
hilo_b.join()
tiempo_threading = time.time() - inicio
print(f"Tiempo total: {tiempo_threading:.2f}s")

# PRUEBA 2: Con multiprocessing (usa múltiples cores reales)
from multiprocessing import Process

def tarea_cpu_process(nombre):
    print(f"[{tiempo()}] {nombre} - inicio (PID: {os.getpid()})")
    resultado = sum(range(20_000_000))
    print(f"[{tiempo()}] {nombre} - fin (resultado: {resultado})")

if __name__ == "__main__":
    print(f"\n=== CON MULTIPROCESSING (múltiples procesos, múltiples cores) ===")
    inicio = time.time()
    proc_a = Process(target=tarea_cpu_process, args=("Process-A",))
    proc_b = Process(target=tarea_cpu_process, args=("Process-B",))
    proc_a.start()
    proc_b.start()
    proc_a.join()
    proc_b.join()
    tiempo_multiproc = time.time() - inicio
    print(f"Tiempo total: {tiempo_multiproc:.2f}s")
    
    print(f"\n=== COMPARACIÓN ===")
    print(f"Threading (1 core efectivo por GIL): {tiempo_threading:.2f}s")
    print(f"Multiprocessing (2+ cores reales): {tiempo_multiproc:.2f}s")
    print(f"Speedup con multiprocessing: {tiempo_threading/tiempo_multiproc:.2f}x")

# Salida típica en máquina con 8 cores:
# Cores disponibles: 8
#
# === CON THREADING ===
# [17:00:00.100] Thread-A - inicio
# [17:00:00.100] Thread-B - inicio
# [17:00:01.450] Thread-A - fin
# [17:00:02.800] Thread-B - fin
# Tiempo total: 2.80s  ← Casi secuencial (1.4s + 1.4s)
#
# === CON MULTIPROCESSING ===
# [17:00:03.000] Process-A - inicio (PID: 12345)
# [17:00:03.000] Process-B - inicio (PID: 12346)
# [17:00:04.400] Process-A - fin
# [17:00:04.400] Process-B - fin
# Tiempo total: 1.40s  ← Paralelo real (máximo de ambos)
#
# === COMPARACIÓN ===
# Threading (1 core efectivo por GIL): 2.80s
# Multiprocessing (2+ cores reales): 1.40s
# Speedup con multiprocessing: 2.00x
```

**Conclusión visual:**

```
SISTEMA: 8 cores disponibles

THREADING (trabajo CPU-bound):
  Core 0: [Thread-A ejecuta]---[Thread-B ejecuta]---
  Core 1: [ocioso]
  Core 2: [ocioso]
  ...
  Core 7: [ocioso]
  
  ⚠️ GIL permite que solo 1 thread ejecute bytecode Python a la vez
  ⚠️ Los threads se ALTERNAN en el mismo core (time-slicing)
  ⚠️ Tiempo total: suma de ambos (~2.8s)
  
MULTIPROCESSING (trabajo CPU-bound):
  Core 0: [Process-A ejecuta en paralelo]----------
  Core 1: [Process-B ejecuta en paralelo]----------
  Core 2: [ocioso]
  ...
  Core 7: [ocioso]
  
  ✅ Cada proceso tiene su propio intérprete y GIL
  ✅ Los procesos ejecutan SIMULTÁNEAMENTE en cores diferentes
  ✅ Tiempo total: máximo de ambos (~1.4s)
```

**Resumen: Threading vs Multiprocessing**

| Característica | Threading | Multiprocessing |
|----------------|-----------|-----------------|
| **Cores usados** | 1 efectivo (GIL) | Múltiples reales |
| **Trabajo I/O-bound** | ✅ Eficiente | ✅ Funciona (overhead innecesario) |
| **Trabajo CPU-bound** | ❌ NO paralelo (GIL) | ✅ Paralelo real |
| **Overhead** | Bajo (~MB) | Alto (~10-50 MB por proceso) |
| **Memoria** | Compartida | Independiente (IPC necesario) |
| **Speedup CPU-bound** | ~1x (sin mejora) | ~Px (P = cores usados) |

**Para el ejemplo original con `time.sleep()`:**
- Threading funciona bien porque sleep() libera el GIL (I/O wait)
- No necesitamos multiprocessing porque no hay trabajo CPU-bound
- Tiempo total: ~2s (máximo de ambos sleeps)

---

**Análisis del modelo:**
- ¿Hay solapamiento? Sí: ambos hilos viven de t=0 a t=2 (aproximadamente)
- ¿Hay ejecución simultánea? **Depende del tipo de trabajo**:
  - I/O-bound (sleep, network, disk): SÍ concurrente, NO necesita múltiples cores
  - CPU-bound (cálculos): NO simultáneo en threading (GIL), SÍ en multiprocessing

**Diferencia clave con asyncio:**

| Característica | `asyncio` | `threading` |
|----------------|-----------|-------------|
| Tipo de concurrencia | Cooperativa (explícita con await) | Preemptiva (OS decide cuándo cambiar) |
| Scheduler | Event loop (Python) | Scheduler del OS |
| Cambio de tarea | Solo en await | En cualquier momento (quantum) |
| Overhead | Bajo (en el mismo proceso) | Medio (context switching del OS) |
| Bloqueo | Si una tarea bloquea, afecta todo | Si un hilo bloquea, otros continúan |
| GIL (Python) | No relevante (un solo hilo) | Limita paralelismo real |

**Caso edge: Python GIL (Global Interpreter Lock)**

El GIL es un mutex que previene que múltiples hilos ejecuten bytecode Python **simultáneamente**.

```python
import threading
import time

def tarea_cpu_bound():
    # Trabajo intensivo de CPU
    resultado = sum(range(10_000_000))
    return resultado

inicio = time.time()

# Con threading (afectado por GIL)
hilo_a = threading.Thread(target=tarea_cpu_bound)
hilo_b = threading.Thread(target=tarea_cpu_bound)

hilo_a.start()
hilo_b.start()

hilo_a.join()
hilo_b.join()

fin = time.time()
print(f"Tiempo con threading: {fin - inicio:.2f}s")
# Resultado típico: ~1.5s (NO es 2x más rápido)

# Comparación con secuencial
inicio = time.time()
tarea_cpu_bound()
tarea_cpu_bound()
fin = time.time()
print(f"Tiempo secuencial: {fin - inicio:.2f}s")
# Resultado típico: ~1.5s (¡casi igual!)
```

**Conclusión del GIL:** En Python, `threading` NO da paralelismo real para tareas CPU-bound.

**¿Cuándo sí ayuda `threading`?**

Cuando las tareas pasan mucho tiempo en esperas I/O **bloqueantes**:

```python
import threading
import requests  # Librería síncrona de HTTP

def descargar_url(url):
    respuesta = requests.get(url)  # Bloqueante, pero libera GIL
    print(f"Descargado {len(respuesta.content)} bytes de {url}")

urls = [
    "https://example.com",
    "https://python.org",
    "https://github.com"
]

hilos = []
for url in urls:
    hilo = threading.Thread(target=descargar_url, args=(url,))
    hilo.start()
    hilos.append(hilo)

for hilo in hilos:
    hilo.join()

# Esto SÍ es más rápido que secuencial porque:
# - requests.get() bloquea el hilo pero libera el GIL
# - Otros hilos pueden ejecutar mientras uno espera I/O
```

**Regla práctica:**
- **I/O-bound con librerías síncronas**: `threading` ayuda (aunque `asyncio` es mejor)
- **CPU-bound**: `threading` NO ayuda en Python (usar `multiprocessing`)

---

#### 1.3.3 Asyncio vs Threading: ¿Cuál usar y cuándo?

Esta es una de las preguntas más importantes al diseñar código concurrente en Python. Vamos a comparar ambos enfoques de manera sistemática.

**Recordatorio rápido:**
- **asyncio:** Concurrencia cooperativa en un solo hilo con event loop
- **threading:** Concurrencia preemptiva con múltiples hilos del OS

---

**Tabla comparativa detallada:**

| Aspecto | `asyncio` | `threading` |
|---------|-----------|-------------|
| **Concurrencia** | Cooperativa (explícita con `await`) | Preemptiva (OS decide cuándo cambiar) |
| **Número de hilos** | 1 hilo | Múltiples hilos (H ≥ 2) |
| **Scheduler** | Event loop (Python) | Scheduler del OS |
| **Cuándo cambia de tarea** | Solo en `await` | Cualquier momento (quantum ~10-100ms) |
| **Overhead** | Muy bajo (~KB por coroutine) | Medio (~1-8 MB por hilo) |
| **Escalabilidad** | Excelente (miles de tareas) | Limitada (decenas/cientos de hilos) |
| **Uso de memoria** | Bajo | Alto (cada hilo consume memoria) |
| **Complejidad código** | Media (requires `async`/`await`) | Baja (código síncrono normal) |
| **Control** | Explícito (tú decides cuándo ceder) | Implícito (OS decide) |
| **Bloqueo accidental** | Si bloqueas, todo se detiene | Si un hilo bloquea, otros continúan |
| **Debugging** | Difícil (traces complejos) | Muy difícil (race conditions, deadlocks) |
| **GIL** | No relevante (1 hilo) | Limita CPU-bound |
| **Ideal para** | I/O-bound con librerías async | I/O-bound con librerías síncronas legacy |

---

**¿Cuándo usar `asyncio`?**

**✅ USA asyncio SI:**

1. **Tienes librerías async disponibles** (aiohttp, asyncpg, aiofiles, etc.)
   ```python
   # Ejemplo: servidor web con muchas conexiones
   import aiohttp
   import asyncio
   
   async def descargar_muchas_urls(urls):
       async with aiohttp.ClientSession() as session:
           tareas = [session.get(url) for url in urls]
           respuestas = await asyncio.gather(*tareas)
           return respuestas
   
   # Puede manejar 1000+ conexiones simultáneas eficientemente
   ```

2. **Necesitas escalar a miles de conexiones simultáneas**
   - Servidores web (FastAPI, aiohttp)
   - Websockets (muchas conexiones persistentes)
   - Chat servers, real-time applications

3. **Trabajo es mayormente I/O-bound** (red, disco, DB)
   ```python
   # Web scraping de 1000 páginas
   async def scrape_all(urls):
       tareas = [scrape_url(url) for url in urls]
       return await asyncio.gather(*tareas)
   # Muy eficiente: 1 hilo, bajo overhead
   ```

4. **Quieres control explícito sobre concurrencia**
   - Sabes exactamente cuándo ceder control (`await`)
   - Reduces race conditions (más predecible)

**❌ NO uses asyncio SI:**

1. **Usas librerías síncronas que no tienen versión async**
   ```python
   # Si usas requests, sqlite3, etc. (sin versión async)
   # asyncio no ayudará, bloqueará el event loop
   ```

2. **Código es CPU-bound** (asyncio no da paralelismo)
   ```python
   # Procesamiento de imágenes, cálculos matemáticos
   # Mejor: multiprocessing
   ```

3. **Proyecto pequeño/simple** sin necesidad de alta concurrencia
   - Overhead de async/await no vale la pena
   - Código secuencial es más simple

---

**¿Cuándo usar `threading`?**

**✅ USA threading SI:**

1. **Usas librerías síncronas/legacy sin versión async**
   ```python
   # Librerías antiguas o sin soporte async
   import threading
   import requests  # Librería síncrona
   
   def descargar(url):
       respuesta = requests.get(url)  # Bloqueante pero libera GIL
       return respuesta.content
   
   # Threading funciona bien aquí
   hilos = [threading.Thread(target=descargar, args=(url,)) for url in urls]
   ```

2. **Pocas tareas concurrentes** (< 100)
   - Threading maneja decenas de hilos sin problema
   - No necesitas escalar a miles

3. **No quieres reescribir código a async**
   - Código legacy funcional
   - Migración gradual

4. **Trabajo es I/O-bound con librerías que liberan GIL**
   - Network I/O (sockets, HTTP)
   - File I/O
   - Database queries (muchas librerías liberan GIL)

**❌ NO uses threading SI:**

1. **Trabajo es CPU-bound**
   ```python
   # GIL previene paralelismo real
   # Mejor: multiprocessing
   ```

2. **Necesitas miles de conexiones simultáneas**
   - Overhead de hilos es alto (~1-8 MB por hilo)
   - Sistema colapsa con 1000+ hilos

3. **Tienes librerías async disponibles**
   - asyncio será más eficiente y escalable

---

**Comparación práctica: Mismo problema, dos soluciones**

**Problema:** Descargar 10 URLs

```python
import time
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

# Simular descarga (tarda 1s cada una)
def simular_descarga(url_id):
    time.sleep(1)  # Simula latencia de red
    return f"Datos de URL {url_id}"

# SOLUCIÓN 1: Con asyncio
import asyncio

async def descargar_async(url_id):
    await asyncio.sleep(1)  # Simula I/O
    return f"Datos de URL {url_id}"

async def main_async():
    print(f"[{tiempo()}] Asyncio: inicio")
    tareas = [descargar_async(i) for i in range(10)]
    resultados = await asyncio.gather(*tareas)
    print(f"[{tiempo()}] Asyncio: fin")
    return resultados

inicio = time.time()
asyncio.run(main_async())
tiempo_async = time.time() - inicio
print(f"Asyncio: {tiempo_async:.2f}s\n")

# Salida:
# [18:00:00.100] Asyncio: inicio
# [18:00:01.102] Asyncio: fin
# Asyncio: 1.00s


# SOLUCIÓN 2: Con threading
import threading

resultados_threading = []

def descargar_thread(url_id):
    resultado = simular_descarga(url_id)
    resultados_threading.append(resultado)

def main_threading():
    print(f"[{tiempo()}] Threading: inicio")
    hilos = []
    for i in range(10):
        hilo = threading.Thread(target=descargar_thread, args=(i,))
        hilo.start()
        hilos.append(hilo)
    
    for hilo in hilos:
        hilo.join()
    print(f"[{tiempo()}] Threading: fin")

inicio = time.time()
main_threading()
tiempo_threading = time.time() - inicio
print(f"Threading: {tiempo_threading:.2f}s\n")

# Salida:
# [18:00:01.200] Threading: inicio
# [18:00:02.203] Threading: fin
# Threading: 1.00s


# COMPARACIÓN:
# - Ambos toman ~1s (aprovechan I/O wait)
# - Asyncio: 1 hilo, ~10 KB overhead total
# - Threading: 10 hilos, ~10-80 MB overhead total
# - Para 10 tareas: similar rendimiento
# - Para 1000 tareas: asyncio escala mucho mejor
```

---

**Árbol de decisión: ¿Qué usar?**

```
¿Tienes librerías ASYNC disponibles?
│
├─ SÍ → ¿Necesitas muchas conexiones simultáneas (>100)?
│       │
│       ├─ SÍ → ASYNCIO ✅
│       │       (Escala a miles de conexiones)
│       │
│       └─ NO → ASYNCIO o THREADING
│               (Ambos funcionan, asyncio más eficiente)
│
└─ NO (solo librerías síncronas)
        │
        ├─ ¿Es trabajo CPU-bound?
        │   │
        │   ├─ SÍ → MULTIPROCESSING ✅
        │   │       (Threading no ayuda por GIL)
        │   │
        │   └─ NO (I/O-bound)
        │           │
        │           ├─ ¿Pocas tareas (<100)?
        │           │   └─ THREADING ✅
        │           │       (Simple, funciona bien)
        │           │
        │           └─ ¿Muchas tareas (>100)?
        │               └─ ASYNCIO + run_in_executor ✅
        │                   (Envuelve librerías síncronas)
```

---

**¿Se pueden combinar asyncio y threading?**

**Respuesta: SÍ**, y es común en aplicaciones reales.

**Caso de uso:** Tienes código async pero necesitas usar una librería síncrona bloqueante.

**Solución:** `loop.run_in_executor()` ejecuta código síncrono en un thread pool sin bloquear el event loop.

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

# Función síncrona bloqueante (ej: librería legacy)
def funcion_sincrona_bloqueante(n):
    time.sleep(2)  # Bloquea (no hay await)
    return f"Resultado {n}"

async def main():
    loop = asyncio.get_running_loop()
    
    # Crear thread pool
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Ejecutar función síncrona en thread pool
        tareas = [
            loop.run_in_executor(executor, funcion_sincrona_bloqueante, i)
            for i in range(3)
        ]
        
        # Esperar resultados (sin bloquear event loop)
        resultados = await asyncio.gather(*tareas)
        print(resultados)

asyncio.run(main())
# Tiempo: ~2s (ejecuta 3 funciones en paralelo en threads)
# Event loop NO se bloquea
```

**Cómo funciona:**
1. Event loop sigue corriendo en el hilo principal
2. Funciones síncronas se ejecutan en threads del pool
3. Cuando terminan, event loop recibe el resultado
4. Mejor de ambos mundos: async + librerías síncronas

**Otros patrones de combinación:**

```python
# 1. Threading con asyncio interno en cada thread
def thread_worker():
    asyncio.run(main_async())  # Cada thread tiene su event loop

# 2. Asyncio con multiprocessing (CPU + I/O bound mix)
async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        resultado = await loop.run_in_executor(
            executor, 
            funcion_cpu_intensiva
        )
```

---

**Casos de uso reales:**

| Escenario | Solución recomendada | Por qué |
|-----------|---------------------|---------|
| **Servidor web** (FastAPI, aiohttp) | asyncio | Miles de conexiones, librerías async |
| **Web scraping** (1000+ URLs) | asyncio + aiohttp | Alta concurrencia, I/O-bound |
| **Web scraping** (10 URLs con requests) | threading | Pocas tareas, librería síncrona |
| **Procesamiento de imágenes** | multiprocessing | CPU-bound |
| **Cliente Discord/Slack bot** | asyncio | Websockets, eventos concurrentes |
| **ETL con DB legacy** | threading | DB síncronas sin async driver |
| **Machine learning training** | multiprocessing + asyncio | CPU (training) + I/O (data loading) |
| **Script simple de backup** | secuencial | Una tarea, simplicidad |

---

**Resumen visual:**

```
ASYNCIO:
  1 hilo principal
  ├─ coroutine_1  ┐
  ├─ coroutine_2  ├─ Event loop gestiona
  ├─ coroutine_3  ├─ Miles posibles
  └─ ...          ┘
  
  Pros: Escalable, bajo overhead
  Cons: Requiere librerías async

THREADING:
  Hilo_1 → Tarea_1
  Hilo_2 → Tarea_2
  Hilo_3 → Tarea_3
  ...     → OS gestiona
  
  Pros: Funciona con código síncrono
  Cons: Overhead alto, no escala a miles

AMBOS COMBINADOS:
  Event loop (asyncio) en hilo principal
  ├─ Coroutines async
  └─ ThreadPoolExecutor
      ├─ Thread_1 → código síncrono
      ├─ Thread_2 → código síncrono
      └─ Thread_3 → código síncrono
  
  Pros: Mejor de ambos mundos
```

---

**Regla de oro final:**

1. **I/O-bound + librerías async disponibles** → `asyncio` ⭐
2. **I/O-bound + solo librerías síncronas** → `threading`
3. **CPU-bound** → `multiprocessing` (nunca threading)
4. **Mix I/O + CPU** → `asyncio` + `run_in_executor` con `ProcessPoolExecutor`
5. **Una tarea simple** → código secuencial (KISS)

---

#### 1.3.2 `ThreadPoolExecutor` - Pool de hilos

**¿Qué es?** Gestiona un pool (conjunto) de hilos reutilizables, evitando crear/destruir hilos constantemente.

**Relación con el modelo:**
- Mantiene H hilos activos (ej: H=4)
- Las tareas se asignan a hilos disponibles
- Si hay más tareas que hilos, las tareas esperan en cola

**Ejemplo mínimo:**

```python
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def tarea(nombre):
    print(f"[{tiempo()}] {nombre} - inicio en hilo {threading.current_thread().name}")
    time.sleep(1)
    print(f"[{tiempo()}] {nombre} - fin")
    return f"Resultado de {nombre}"

print(f"[{tiempo()}] Main: creando pool con 2 hilos")

# Crear pool con 2 hilos
with ThreadPoolExecutor(max_workers=2) as executor:
    print(f"[{tiempo()}] Main: enviando 4 tareas al pool")
    
    # Enviar 4 tareas (más tareas que hilos)
    futures = [executor.submit(tarea, f"Tarea-{i}") for i in range(4)]
    
    # Obtener resultados
    for i, future in enumerate(futures):
        resultado = future.result()
        print(f"[{tiempo()}] Main: recibió {resultado}")

print(f"[{tiempo()}] Main: todas las tareas completadas")

# Imprime algo como:
# [19:00:00.100] Main: creando pool con 2 hilos
# [19:00:00.101] Main: enviando 4 tareas al pool
# [19:00:00.102] Tarea-0 - inicio en hilo ThreadPoolExecutor-0_0
# [19:00:00.102] Tarea-1 - inicio en hilo ThreadPoolExecutor-0_1
# (espera ~1s - ambos hilos trabajando)
# [19:00:01.103] Tarea-0 - fin
# [19:00:01.103] Tarea-1 - fin
# [19:00:01.103] Main: recibió Resultado de Tarea-0
# [19:00:01.103] Tarea-2 - inicio en hilo ThreadPoolExecutor-0_0  ← Reutiliza hilo
# [19:00:01.104] Main: recibió Resultado de Tarea-1
# [19:00:01.104] Tarea-3 - inicio en hilo ThreadPoolExecutor-0_1  ← Reutiliza hilo
# (espera ~1s - ambos hilos trabajando de nuevo)
# [19:00:02.104] Tarea-2 - fin
# [19:00:02.104] Tarea-3 - fin
# [19:00:02.104] Main: recibió Resultado de Tarea-2
# [19:00:02.104] Main: recibió Resultado de Tarea-3
# [19:00:02.104] Main: todas las tareas completadas
```

**Análisis temporal:**

```
t=0.100: Main crea pool con 2 hilos
t=0.101: Main envía 4 tareas a la cola del pool
t=0.102: Pool asigna Tarea-0 a Hilo-0
t=0.102: Pool asigna Tarea-1 a Hilo-1
         Tarea-2 y Tarea-3 esperan en cola (no hay hilos disponibles)
t=0.102-1.103: Ambos hilos trabajando (sleep 1s)
t=1.103: Tarea-0 y Tarea-1 terminan
t=1.103: Pool asigna Tarea-2 a Hilo-0 (reutiliza)
t=1.104: Pool asigna Tarea-3 a Hilo-1 (reutiliza)
t=1.104-2.104: Ambos hilos trabajando de nuevo
t=2.104: Tarea-2 y Tarea-3 terminan
Tiempo total: ~2s (4 tareas / 2 hilos = 2 rondas)
```

**Ventajas de ThreadPoolExecutor vs crear hilos manualmente:**
- Reutilización de hilos (menor overhead)
- Límite de concurrencia (max_workers previene sobrecarga)
- API más simple para muchas tareas
- Gestión automática del ciclo de vida de los hilos

---

**Comparación completa: Asyncio vs Threading vs ThreadPoolExecutor**

Veamos el **mismo problema** (ejecutar 4 tareas de 1s cada una) con los **tres enfoques**:

```python
import asyncio
import threading
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

# Función para simular trabajo I/O
def trabajo_io(nombre):
    time.sleep(1)
    return f"Resultado de {nombre}"

async def trabajo_io_async(nombre):
    await asyncio.sleep(1)
    return f"Resultado de {nombre}"


# ============================================================
# OPCIÓN 1: ASYNCIO (1 hilo, event loop)
# ============================================================
async def opcion_asyncio():
    print(f"\n{'='*50}")
    print(f"[{tiempo()}] ASYNCIO: inicio")
    print(f"{'='*50}")
    
    tareas = [trabajo_io_async(f"Tarea-{i}") for i in range(4)]
    resultados = await asyncio.gather(*tareas)
    
    print(f"[{tiempo()}] ASYNCIO: fin")
    print(f"Resultados: {resultados}")
    return "asyncio"

inicio = time.time()
asyncio.run(opcion_asyncio())
tiempo_asyncio = time.time() - inicio
print(f"⏱️  Tiempo total: {tiempo_asyncio:.2f}s\n")

# Salida:
# ==================================================
# [19:00:00.100] ASYNCIO: inicio
# ==================================================
# [19:00:01.102] ASYNCIO: fin
# Resultados: ['Resultado de Tarea-0', 'Resultado de Tarea-1', ...]
# ⏱️  Tiempo total: 1.00s


# ============================================================
# OPCIÓN 2: THREADING MANUAL (4 hilos creados explícitamente)
# ============================================================
def opcion_threading_manual():
    print(f"\n{'='*50}")
    print(f"[{tiempo()}] THREADING MANUAL: inicio")
    print(f"{'='*50}")
    
    resultados = []
    
    def worker(nombre):
        resultado = trabajo_io(nombre)
        resultados.append(resultado)
        print(f"[{tiempo()}] {nombre} completado")
    
    # Crear 4 hilos (1 por tarea)
    hilos = []
    for i in range(4):
        hilo = threading.Thread(target=worker, args=(f"Tarea-{i}",))
        hilo.start()
        hilos.append(hilo)
    
    # Esperar a todos
    for hilo in hilos:
        hilo.join()
    
    print(f"[{tiempo()}] THREADING MANUAL: fin")
    print(f"Resultados: {resultados}")

inicio = time.time()
opcion_threading_manual()
tiempo_threading = time.time() - inicio
print(f"⏱️  Tiempo total: {tiempo_threading:.2f}s\n")

# Salida:
# ==================================================
# [19:00:01.200] THREADING MANUAL: inicio
# ==================================================
# [19:00:02.202] Tarea-0 completado
# [19:00:02.202] Tarea-1 completado
# [19:00:02.202] Tarea-2 completado
# [19:00:02.202] Tarea-3 completado
# [19:00:02.202] THREADING MANUAL: fin
# Resultados: [...]
# ⏱️  Tiempo total: 1.00s


# ============================================================
# OPCIÓN 3: THREADPOOLEXECUTOR (pool de 2 hilos)
# ============================================================
def opcion_threadpool():
    print(f"\n{'='*50}")
    print(f"[{tiempo()}] THREADPOOLEXECUTOR: inicio (pool de 2 hilos)")
    print(f"{'='*50}")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(trabajo_io, f"Tarea-{i}") for i in range(4)]
        
        resultados = []
        for i, future in enumerate(futures):
            resultado = future.result()
            resultados.append(resultado)
            print(f"[{tiempo()}] Main recibió {resultado}")
    
    print(f"[{tiempo()}] THREADPOOLEXECUTOR: fin")
    print(f"Resultados: {resultados}")

inicio = time.time()
opcion_threadpool()
tiempo_threadpool = time.time() - inicio
print(f"⏱️  Tiempo total: {tiempo_threadpool:.2f}s\n")

# Salida:
# ==================================================
# [19:00:02.300] THREADPOOLEXECUTOR: inicio (pool de 2 hilos)
# ==================================================
# [19:00:03.302] Main recibió Resultado de Tarea-0
# [19:00:03.302] Main recibió Resultado de Tarea-1
# [19:00:04.303] Main recibió Resultado de Tarea-2
# [19:00:04.303] Main recibió Resultado de Tarea-3
# [19:00:04.303] THREADPOOLEXECUTOR: fin
# Resultados: [...]
# ⏱️  Tiempo total: 2.00s


# ============================================================
# COMPARACIÓN FINAL
# ============================================================
print(f"\n{'='*50}")
print("RESUMEN DE COMPARACIÓN")
print(f"{'='*50}")
print(f"Asyncio (1 hilo):                    {tiempo_asyncio:.2f}s")
print(f"Threading Manual (4 hilos):          {tiempo_threading:.2f}s")
print(f"ThreadPoolExecutor (pool de 2):      {tiempo_threadpool:.2f}s")
print(f"\nMemoria aproximada:")
print(f"  Asyncio:          ~10 KB  (4 coroutines)")
print(f"  Threading Manual: ~32 MB  (4 hilos creados)")
print(f"  ThreadPool:       ~16 MB  (2 hilos reutilizados)")
```

---

**Tabla comparativa de los tres enfoques:**

| Característica | `asyncio` | `threading` (manual) | `ThreadPoolExecutor` |
|----------------|-----------|----------------------|----------------------|
| **Tiempo (4 tareas 1s)** | ~1.0s | ~1.0s | ~2.0s (pool de 2) |
| **Hilos creados** | 1 | 4 (1 por tarea) | 2 (reutilizados) |
| **Memoria** | ~10 KB | ~32 MB | ~16 MB |
| **Overhead creación** | Muy bajo | Alto (crear 4 hilos) | Medio (crear 2 hilos) |
| **Reutilización** | N/A (coroutines) | ❌ No | ✅ Sí |
| **Límite concurrencia** | Manual (gather/semáforos) | Manual (crear menos hilos) | Automático (max_workers) |
| **Código** | Requires async/await | Verboso (start/join) | Conciso |
| **Escalabilidad** | Excelente (miles) | Mala (cientos máx) | Buena (decenas) |
| **Control fino** | Alto (create_task) | Alto (Thread objects) | Medio (submit/map) |
| **API** | Moderna (async) | Tradicional | Moderna (futures) |

---

**Análisis temporal comparado:**

```
ASYNCIO (1 hilo, 4 coroutines):
t=0.0: Las 4 coroutines inician casi simultáneamente
t=0.0-1.0: Todas en wait (sleep) - event loop ocioso
t=1.0: Las 4 terminan casi simultáneamente
Tiempo: 1.0s

THREADING MANUAL (4 hilos):
t=0.0: Los 4 hilos inician casi simultáneamente
t=0.0-1.0: Todos en wait (sleep, liberan GIL)
t=1.0: Los 4 terminan casi simultáneamente
Tiempo: 1.0s
Overhead: Creación de 4 hilos (~8 MB cada uno)

THREADPOOLEXECUTOR (pool de 2 hilos, 4 tareas):
t=0.0: Tarea-0 y Tarea-1 inician (hilos 0 y 1)
       Tarea-2 y Tarea-3 esperan en cola
t=0.0-1.0: Hilos 0 y 1 en wait
t=1.0: Tarea-0 y Tarea-1 terminan
       Tarea-2 asignada a Hilo-0 (reutiliza)
       Tarea-3 asignada a Hilo-1 (reutiliza)
t=1.0-2.0: Hilos 0 y 1 en wait (segunda ronda)
t=2.0: Tarea-2 y Tarea-3 terminan
Tiempo: 2.0s (4 tareas / 2 hilos = 2 rondas)
Overhead: Creación de solo 2 hilos (~4 MB cada uno)
```

---

**¿Cuándo usar cada uno?**

**Usa `asyncio` SI:**
- ✅ Tienes librerías async (aiohttp, asyncpg)
- ✅ Necesitas escalar a miles de conexiones
- ✅ Quieres máxima eficiencia de memoria
- ✅ Control explícito de concurrencia

**Usa `threading` (manual) SI:**
- ✅ Pocas tareas (< 10)
- ✅ Cada tarea necesita estado/control individual
- ✅ Necesitas flexibilidad máxima (start/join/interrupt)
- ❌ No lo uses para muchas tareas (overhead alto)

**Usa `ThreadPoolExecutor` SI:**
- ✅ Muchas tareas (10-100)
- ✅ Librerías síncronas sin versión async
- ✅ Quieres limitar concurrencia (max_workers)
- ✅ No necesitas control fino de cada hilo
- ✅ Reutilización de hilos es importante
- ❌ No lo uses para miles de tareas (usa asyncio)

**Ejemplo práctico de decisión:**

```python
# Caso: Descargar 100 URLs

# OPCIÓN A: asyncio (mejor para este caso)
async def descargar_100_urls():
    async with aiohttp.ClientSession() as session:
        tareas = [session.get(url) for url in urls]
        return await asyncio.gather(*tareas)
# Tiempo: ~5s, Memoria: ~1 MB

# OPCIÓN B: ThreadPoolExecutor (alternativa sólida)
def descargar_100_urls():
    with ThreadPoolExecutor(max_workers=10) as executor:
        return list(executor.map(requests.get, urls))
# Tiempo: ~10s, Memoria: ~80 MB (10 hilos)

# OPCIÓN C: Threading manual (NO RECOMENDADO)
def descargar_100_urls():
    hilos = [Thread(target=requests.get, args=(url,)) for url in urls]
    # 100 hilos! Sistema colapsará
# Tiempo: ~15s, Memoria: ~800 MB (100 hilos)
```

---

**Resumen visual:**

```
ASYNCIO:
  [1 hilo]
    └─ [4 coroutines ejecutan concurrentemente]
  Tiempo: 1s
  
THREADING MANUAL:
  [4 hilos creados]
    ├─ Hilo-0
    ├─ Hilo-1
    ├─ Hilo-2
    └─ Hilo-3
  Tiempo: 1s (overhead creación alta)
  
THREADPOOLEXECUTOR:
  [Pool de 2 hilos]
    ├─ Hilo-0: Tarea-0 → Tarea-2
    └─ Hilo-1: Tarea-1 → Tarea-3
  Tiempo: 2s (reutilización, menor overhead)
```

---

**Regla práctica:**

1. **I/O-bound + librerías async** → `asyncio` ⭐
2. **I/O-bound + librerías síncronas + muchas tareas** → `ThreadPoolExecutor` ⭐
3. **I/O-bound + librerías síncronas + pocas tareas** → `threading` manual
4. **CPU-bound** → `ProcessPoolExecutor` (no threading)
5. **Control fino necesario** → `threading` manual o `asyncio.create_task()`

---

**Código mínimo para cada enfoque:**

```python
# Asyncio (más conciso)
await asyncio.gather(*[tarea() for _ in range(100)])

# ThreadPoolExecutor (balance)
with ThreadPoolExecutor(max_workers=10) as ex:
    list(ex.map(tarea, range(100)))

# Threading manual (más verboso)
hilos = [Thread(target=tarea, args=(i,)) for i in range(100)]
for h in hilos: h.start()
for h in hilos: h.join()
```

**Caso edge: max_workers y número de cores**

```python
import os

# ¿Cuántos hilos usar?
num_cpus = os.cpu_count()  # Ej: 8 cores

# Para tareas I/O-bound: puede ser mucho mayor que num_cpus
executor_io = ThreadPoolExecutor(max_workers=num_cpus * 5)  # 40 hilos

# Para tareas CPU-bound: no ayuda por el GIL
executor_cpu = ThreadPoolExecutor(max_workers=num_cpus)  # Desperdicio
```

**Regla:** Para CPU-bound en Python, `ThreadPoolExecutor` no da paralelismo real (GIL).

---

#### 1.3.3 Threading vs Asyncio: ¿Cuál usar?

**Tabla comparativa:**

| Criterio | `asyncio` | `threading` |
|----------|-----------|-------------|
| **Tipo de tareas** | I/O-bound con librerías async | I/O-bound con librerías síncronas |
| **Complejidad** | Media (requires async/await) | Baja (código síncrono normal) |
| **Escalabilidad** | Alta (miles de corrutinas) | Media (decenas/cientos de hilos) |
| **Overhead** | Muy bajo | Medio (cada hilo ~1-8 MB RAM) |
| **Control** | Cooperativo (explícito) | Preemptivo (automático) |
| **GIL** | No relevante | Limita paralelismo |
| **Debugging** | Difícil (traces complejos) | Más difícil (race conditions) |

**Recomendación general:**

```python
# ✅ Usar asyncio SI:
# - Tienes librerías async disponibles (aiohttp, asyncpg, etc.)
# - Necesitas escalar a miles de conexiones simultáneas
# - Tareas son mayormente espera I/O

# ✅ Usar threading SI:
# - Usas librerías síncronas que no tienen versión async
# - Pocas tareas concurrentes (< 100)
# - Código legacy que no quieres reescribir

# ✅ Usar multiprocessing SI:
# - Tareas son CPU-bound (cálculos intensivos)
# - Necesitas paralelismo real (aprovechar múltiples cores)
```

---

### 1.4 Librería `multiprocessing` y `concurrent.futures.ProcessPoolExecutor`: Paralelismo Real

**Propósito:** Implementar **paralelismo físico real** mediante múltiples procesos del OS.

**Relación con el modelo:**
- Permite ejecución simultánea física: ∃ t: |ExecutingAt(t)| ≥ 2
- Usa P ≥ 2 cores
- Cada proceso tiene memoria independiente (no compartida)
- **Evita el GIL**: cada proceso tiene su propio intérprete Python
- Modelo correspondiente: Sección 6 (Paralelo)

**Componentes principales:**

#### 1.4.1 `Process` - Crear un proceso

**¿Qué es?** Similar a `Thread`, pero crea un proceso del OS completo con memoria independiente.

**Ejemplo mínimo:**

```python
from multiprocessing import Process
import os
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def tarea(nombre, tamaño):
    print(f"[{tiempo()}] {nombre} - PID: {os.getpid()} - INICIO")
    resultado = sum(range(tamaño))  # CPU-bound
    print(f"[{tiempo()}] {nombre} - PID: {os.getpid()} - FIN (resultado: {resultado})")

if __name__ == "__main__":  # Importante en multiprocessing
    print(f"[{tiempo()}] Main - PID: {os.getpid()} - Cores disponibles: {os.cpu_count()}")
    print(f"[{tiempo()}] Main - Creando procesos...")
    
    # Crear procesos con diferentes cargas de trabajo
    proceso_a = Process(target=tarea, args=("Proceso-A", 15_000_000))
    proceso_b = Process(target=tarea, args=("Proceso-B", 10_000_000))
    
    # Iniciar procesos
    print(f"[{tiempo()}] Main - Iniciando procesos...")
    proceso_a.start()
    proceso_b.start()
    
    # Esperar a que terminen
    proceso_a.join()
    proceso_b.join()
    
    print(f"[{tiempo()}] Main - Todos los procesos terminaron")

# Imprime algo como:
# [20:00:00.100] Main - PID: 12340 - Cores disponibles: 8
# [20:00:00.101] Main - Creando procesos...
# [20:00:00.102] Main - Iniciando procesos...
# [20:00:00.150] Proceso-A - PID: 12345 - INICIO
# [20:00:00.151] Proceso-B - PID: 12346 - INICIO
# [20:00:00.450] Proceso-B - PID: 12346 - FIN (resultado: 49999995000000)
# [20:00:00.650] Proceso-A - PID: 12345 - FIN (resultado: 112499992500000)
# [20:00:00.651] Main - Todos los procesos terminaron
# 
# Nota: Proceso-B termina ANTES que Proceso-A (tiene menos trabajo)
#       Ambos ejecutan SIMULTÁNEAMENTE en cores diferentes
```

**Diferencia clave con threading:**

```python
import time
from threading import Thread
from multiprocessing import Process

def tarea_cpu():
    resultado = sum(range(20_000_000))

# Con threading (afectado por GIL)
inicio = time.time()
t1 = Thread(target=tarea_cpu)
t2 = Thread(target=tarea_cpu)
t1.start(); t2.start()
t1.join(); t2.join()
tiempo_threading = time.time() - inicio

# Con multiprocessing (sin GIL, paralelismo real)
if __name__ == "__main__":
    inicio = time.time()
    p1 = Process(target=tarea_cpu)
    p2 = Process(target=tarea_cpu)
    p1.start(); p2.start()
    p1.join(); p2.join()
    tiempo_multiproc = time.time() - inicio

    print(f"Threading: {tiempo_threading:.2f}s")
    print(f"Multiprocessing: {tiempo_multiproc:.2f}s")
    # Ejemplo de resultado en máquina con P=4:
    # Threading: 3.5s
    # Multiprocessing: 1.8s  (casi 2x más rápido)
```

**Análisis del modelo:**
- Con threading: exec(τ₁) ∩ exec(τ₂) = ∅ (nunca simultáneo por GIL)
- Con multiprocessing: exec(τ₁) ∩ exec(τ₂) ≠ ∅ (ejecución simultánea real)

---

#### 1.4.2 `ProcessPoolExecutor` - Pool de procesos

**¿Qué es?** Similar a `ThreadPoolExecutor`, pero con procesos en lugar de hilos.

**Ejemplo mínimo:**

```python
from concurrent.futures import ProcessPoolExecutor
import time
import os
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def tarea_cpu_bound(n):
    print(f"[{tiempo()}] Procesando {n:,} elementos en PID {os.getpid()}")
    resultado = sum(range(n))
    print(f"[{tiempo()}] PID {os.getpid()} terminó: resultado = {resultado:,}")
    return resultado

if __name__ == "__main__":
    datos = [10_000_000, 20_000_000, 30_000_000, 40_000_000]
    
    print(f"Cores disponibles: {os.cpu_count()}")
    print(f"\n{'='*60}")
    print("EJECUCIÓN SECUENCIAL (baseline)")
    print(f"{'='*60}")
    
    # Secuencial (baseline)
    inicio = time.time()
    resultados_seq = [tarea_cpu_bound(n) for n in datos]
    tiempo_seq = time.time() - inicio
    print(f"\n⏱️  Tiempo secuencial: {tiempo_seq:.2f}s")
    
    print(f"\n{'='*60}")
    print("EJECUCIÓN PARALELA (4 cores)")
    print(f"{'='*60}")
    
    # Paralelo con ProcessPoolExecutor
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        resultados_par = list(executor.map(tarea_cpu_bound, datos))
    tiempo_par = time.time() - inicio
    print(f"\n⏱️  Tiempo paralelo: {tiempo_par:.2f}s")
    print(f"⚡ Speedup: {tiempo_seq/tiempo_par:.2f}x")
    
# Salida típica en máquina con 8 cores:
#
# Cores disponibles: 8
#
# ============================================================
# EJECUCIÓN SECUENCIAL (baseline)
# ============================================================
# [20:05:00.100] Procesando 10,000,000 elementos en PID 12340
# [20:05:00.450] PID 12340 terminó: resultado = 49,999,995,000,000
# [20:05:00.450] Procesando 20,000,000 elementos en PID 12340
# [20:05:01.150] PID 12340 terminó: resultado = 199,999,990,000,000
# [20:05:01.150] Procesando 30,000,000 elementos en PID 12340
# [20:05:02.200] PID 12340 terminó: resultado = 449,999,985,000,000
# [20:05:02.200] Procesando 40,000,000 elementos en PID 12340
# [20:05:03.650] PID 12340 terminó: resultado = 799,999,980,000,000
#
# ⏱️  Tiempo secuencial: 3.55s
#
# ============================================================
# EJECUCIÓN PARALELA (4 cores)
# ============================================================
# [20:05:03.700] Procesando 10,000,000 elementos en PID 12345
# [20:05:03.701] Procesando 20,000,000 elementos en PID 12346
# [20:05:03.702] Procesando 30,000,000 elementos en PID 12347
# [20:05:03.703] Procesando 40,000,000 elementos en PID 12348
# [20:05:04.050] PID 12345 terminó: resultado = 49,999,995,000,000     ← Termina primero (menos trabajo)
# [20:05:04.750] PID 12346 terminó: resultado = 199,999,990,000,000    ← Termina segundo
# [20:05:05.800] PID 12347 terminó: resultado = 449,999,985,000,000    ← Termina tercero
# [20:05:07.250] PID 12348 terminó: resultado = 799,999,980,000,000    ← Termina último (más trabajo)
#
# ⏱️  Tiempo paralelo: 3.55s
# ⚡ Speedup: 1.00x
#
# Nota: Los 4 procesos inician CASI SIMULTÁNEAMENTE (diferencia de ~1-3ms)
#       Pero terminan en DIFERENTE ORDEN según su carga de trabajo
#       Tiempo total = tiempo de la tarea más lenta (no la suma)
```

**Análisis del modelo:**
- Paralelismo real: los 4 procesos ejecutan simultáneamente en P=4 cores
- Speedup: ~P veces más rápido (con overhead de IPC)
- Los procesos terminan en orden de menor a mayor trabajo, no en orden de creación

---

**Ejemplo COMPLEJO: Procesamiento Paralelo Intensivo**

Este ejemplo demuestra el verdadero poder del paralelismo con una carga de trabajo realista y pesada:

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os
import math
from datetime import datetime
import random

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def procesar_datos_complejos(tarea_id, tamaño_datos, complejidad):
    """
    Simula procesamiento intensivo de CPU:
    - Cálculos matemáticos complejos
    - Múltiples iteraciones
    - Diferentes cargas de trabajo
    """
    pid = os.getpid()
    print(f"[{tiempo()}] 🚀 Tarea-{tarea_id} (PID {pid}): INICIO - {tamaño_datos:,} datos, complejidad {complejidad}")
    
    # Simulación de trabajo CPU-intensivo
    inicio_tarea = time.time()
    resultado = 0
    
    # Fase 1: Cálculos matemáticos pesados
    for i in range(tamaño_datos):
        resultado += math.sqrt(i) * math.sin(i) * math.cos(i)
        if i % 1_000_000 == 0 and i > 0:
            # Progreso cada millón de iteraciones
            progreso = (i / tamaño_datos) * 100
            if progreso % 25 == 0:  # Log cada 25%
                print(f"[{tiempo()}]    Tarea-{tarea_id} (PID {pid}): {progreso:.0f}% completado")
    
    # Fase 2: Procesamiento adicional según complejidad
    for _ in range(complejidad):
        temp = sum(range(1_000_000))
        resultado += temp * 0.0001
    
    tiempo_tarea = time.time() - inicio_tarea
    print(f"[{tiempo()}] ✅ Tarea-{tarea_id} (PID {pid}): COMPLETADA en {tiempo_tarea:.2f}s - resultado = {resultado:.2f}")
    
    return {
        'tarea_id': tarea_id,
        'pid': pid,
        'tiempo': tiempo_tarea,
        'resultado': resultado,
        'tamaño': tamaño_datos,
        'complejidad': complejidad
    }


if __name__ == "__main__":
    # Configuración: 8 tareas con diferentes cargas
    tareas = [
        (1, 3_000_000, 3),   # Tarea ligera
        (2, 5_000_000, 5),   # Tarea mediana
        (3, 8_000_000, 4),   # Tarea pesada
        (4, 4_000_000, 6),   # Tarea mediana con alta complejidad
        (5, 6_000_000, 2),   # Tarea mediana-pesada, baja complejidad
        (6, 2_000_000, 8),   # Tarea ligera, muy alta complejidad
        (7, 7_000_000, 3),   # Tarea pesada
        (8, 5_000_000, 4),   # Tarea mediana
    ]
    
    num_cores = os.cpu_count()
    max_workers = min(4, num_cores)  # Usar máximo 4 cores
    
    print("="*80)
    print(f"PROCESAMIENTO PARALELO INTENSIVO")
    print("="*80)
    print(f"Sistema: {num_cores} cores disponibles")
    print(f"Configuración: {len(tareas)} tareas, usando {max_workers} procesos en paralelo")
    print(f"Carga total: {sum(t[1] for t in tareas):,} iteraciones")
    print("="*80)
    
    # ============================================================
    # OPCIÓN 1: EJECUCIÓN SECUENCIAL (para comparación)
    # ============================================================
    print(f"\n[{tiempo()}] 📊 INICIANDO EJECUCIÓN SECUENCIAL...")
    print("-"*80)
    
    inicio_seq = time.time()
    resultados_seq = []
    for tarea_id, tamaño, complejidad in tareas:
        resultado = procesar_datos_complejos(tarea_id, tamaño, complejidad)
        resultados_seq.append(resultado)
    tiempo_seq = time.time() - inicio_seq
    
    print("-"*80)
    print(f"⏱️  SECUENCIAL COMPLETADO: {tiempo_seq:.2f}s")
    print("="*80)
    
    # ============================================================
    # OPCIÓN 2: EJECUCIÓN PARALELA CON ProcessPoolExecutor
    # ============================================================
    print(f"\n[{tiempo()}] ⚡ INICIANDO EJECUCIÓN PARALELA (ProcessPoolExecutor)...")
    print("-"*80)
    
    inicio_par = time.time()
    resultados_par = []
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Enviar todas las tareas al pool
        futures = {
            executor.submit(procesar_datos_complejos, tid, tam, comp): tid
            for tid, tam, comp in tareas
        }
        
        # Procesar resultados conforme van completando (no en orden)
        orden_completacion = []
        for future in as_completed(futures):
            tarea_id = futures[future]
            resultado = future.result()
            resultados_par.append(resultado)
            orden_completacion.append(tarea_id)
    
    tiempo_par = time.time() - inicio_par
    
    print("-"*80)
    print(f"⏱️  PARALELO COMPLETADO: {tiempo_par:.2f}s")
    print(f"📋 Orden de completación: {orden_completacion}")
    print(f"   (Nota: NO es el orden de envío [1,2,3,4,5,6,7,8])")
    print("="*80)
    
    # ============================================================
    # ANÁLISIS Y COMPARACIÓN
    # ============================================================
    print(f"\n{'='*80}")
    print("ANÁLISIS DE RENDIMIENTO")
    print("="*80)
    print(f"Tiempo secuencial:  {tiempo_seq:.2f}s")
    print(f"Tiempo paralelo:    {tiempo_par:.2f}s")
    print(f"⚡ Speedup:          {tiempo_seq/tiempo_par:.2f}x")
    print(f"💾 Cores utilizados: {max_workers} de {num_cores} disponibles")
    print(f"📈 Eficiencia:       {(tiempo_seq/tiempo_par)/max_workers*100:.1f}%")
    print("="*80)
    
    # Análisis por tarea
    print(f"\nDETALLE POR TAREA:")
    print("-"*80)
    print(f"{'Tarea':<8} {'Tamaño':>12} {'Complej':>8} {'Tiempo':>10} {'PID':>8}")
    print("-"*80)
    for r in sorted(resultados_par, key=lambda x: x['tarea_id']):
        print(f"Tarea-{r['tarea_id']:<3} {r['tamaño']:>12,} {r['complejidad']:>8} "
              f"{r['tiempo']:>9.2f}s {r['pid']:>8}")
    print("="*80)
    
    print(f"\n💡 OBSERVACIONES CLAVE:")
    print(f"   1. Las tareas NO terminan en orden de envío")
    print(f"   2. Cada tarea usa un PID diferente (proceso independiente)")
    print(f"   3. Múltiples tareas ejecutan SIMULTÁNEAMENTE")
    print(f"   4. Speedup cercano a {max_workers}x (paralelismo real)")
    print(f"   5. Tiempo total = tiempo de la tarea MÁS LENTA, no la suma")

# ============================================================================
# SALIDA TÍPICA EN MÁQUINA CON 8 CORES:
# ============================================================================
#
# ================================================================================
# PROCESAMIENTO PARALELO INTENSIVO
# ================================================================================
# Sistema: 8 cores disponibles
# Configuración: 8 tareas, usando 4 procesos en paralelo
# Carga total: 40,000,000 iteraciones
# ================================================================================
#
# [20:10:00.100] 📊 INICIANDO EJECUCIÓN SECUENCIAL...
# --------------------------------------------------------------------------------
# [20:10:00.101] 🚀 Tarea-1 (PID 12340): INICIO - 3,000,000 datos, complejidad 3
# [20:10:02.450] ✅ Tarea-1 (PID 12340): COMPLETADA en 2.35s - resultado = 1234.56
# [20:10:02.451] 🚀 Tarea-2 (PID 12340): INICIO - 5,000,000 datos, complejidad 5
# [20:10:06.200] ✅ Tarea-2 (PID 12340): COMPLETADA en 3.75s - resultado = 2345.67
# ... (continúa secuencialmente)
# --------------------------------------------------------------------------------
# ⏱️  SECUENCIAL COMPLETADO: 28.50s
# ================================================================================
#
# [20:10:28.650] ⚡ INICIANDO EJECUCIÓN PARALELA (ProcessPoolExecutor)...
# --------------------------------------------------------------------------------
# [20:10:28.700] 🚀 Tarea-1 (PID 12341): INICIO - 3,000,000 datos, complejidad 3
# [20:10:28.701] 🚀 Tarea-2 (PID 12342): INICIO - 5,000,000 datos, complejidad 5
# [20:10:28.702] 🚀 Tarea-3 (PID 12343): INICIO - 8,000,000 datos, complejidad 4
# [20:10:28.703] 🚀 Tarea-4 (PID 12344): INICIO - 4,000,000 datos, complejidad 6
# [20:10:31.050] ✅ Tarea-1 (PID 12341): COMPLETADA en 2.35s - resultado = 1234.56
# [20:10:31.051] 🚀 Tarea-5 (PID 12341): INICIO - 6,000,000 datos, complejidad 2  ← Reutiliza PID 12341
# [20:10:32.950] ✅ Tarea-4 (PID 12344): COMPLETADA en 4.25s - resultado = 3456.78
# [20:10:32.951] 🚀 Tarea-6 (PID 12344): INICIO - 2,000,000 datos, complejidad 8  ← Reutiliza PID 12344
# [20:10:33.450] ✅ Tarea-2 (PID 12342): COMPLETADA en 4.75s - resultado = 2345.67
# [20:10:33.451] 🚀 Tarea-7 (PID 12342): INICIO - 7,000,000 datos, complejidad 3  ← Reutiliza PID 12342
# [20:10:35.200] ✅ Tarea-6 (PID 12344): COMPLETADA en 2.25s - resultado = 4567.89
# [20:10:35.201] 🚀 Tarea-8 (PID 12344): INICIO - 5,000,000 datos, complejidad 4  ← Reutiliza PID 12344
# [20:10:36.100] ✅ Tarea-3 (PID 12343): COMPLETADA en 7.40s - resultado = 5678.90
# [20:10:36.500] ✅ Tarea-5 (PID 12341): COMPLETADA en 5.45s - resultado = 6789.01
# [20:10:38.950] ✅ Tarea-7 (PID 12342): COMPLETADA en 5.50s - resultado = 7890.12
# [20:10:39.100] ✅ Tarea-8 (PID 12344): COMPLETADA en 3.90s - resultado = 8901.23
# --------------------------------------------------------------------------------
# ⏱️  PARALELO COMPLETADO: 10.40s
# 📋 Orden de completación: [1, 4, 2, 6, 3, 5, 7, 8]
#    (Nota: NO es el orden de envío [1,2,3,4,5,6,7,8])
# ================================================================================
#
# ================================================================================
# ANÁLISIS DE RENDIMIENTO
# ================================================================================
# Tiempo secuencial:  28.50s
# Tiempo paralelo:    10.40s
# ⚡ Speedup:          2.74x
# 💾 Cores utilizados: 4 de 8 disponibles
# 📈 Eficiencia:       68.5%
# ================================================================================
#
# DETALLE POR TAREA:
# --------------------------------------------------------------------------------
# Tarea    Tamaño    Complej     Tiempo      PID
# --------------------------------------------------------------------------------
# Tarea-1   3,000,000        3      2.35s    12341
# Tarea-2   5,000,000        5      4.75s    12342
# Tarea-3   8,000,000        4      7.40s    12343
# Tarea-4   4,000,000        6      4.25s    12344
# Tarea-5   6,000,000        2      5.45s    12341
# Tarea-6   2,000,000        8      2.25s    12344
# Tarea-7   7,000,000        3      5.50s    12342
# Tarea-8   5,000,000        4      3.90s    12344
# ================================================================================
#
# 💡 OBSERVACIONES CLAVE:
#    1. Las tareas NO terminan en orden de envío
#    2. Cada tarea usa un PID diferente (proceso independiente)
#    3. Múltiples tareas ejecutan SIMULTÁNEAMENTE
#    4. Speedup cercano a 4x (paralelismo real)
#    5. Tiempo total = tiempo de la tarea MÁS LENTA, no la suma
```

**Análisis del ejemplo complejo:**

```
EJECUCIÓN SECUENCIAL:
Timeline: [Tarea-1]--[Tarea-2]--[Tarea-3]--[Tarea-4]--[Tarea-5]--[Tarea-6]--[Tarea-7]--[Tarea-8]
Tiempo:   ████████████████████████████ (28.5s)
Cores:    Solo 1 core trabajando, 7 ociosos

EJECUCIÓN PARALELA (4 cores):
Core 0:   [Tarea-1]-----[Tarea-5]-------------
Core 1:   [Tarea-2]----------[Tarea-7]--------
Core 2:   [Tarea-3 (más lenta)]---------------
Core 3:   [Tarea-4]---[Tarea-6]-[Tarea-8]-----
Tiempo:   ██████████ (10.4s)
          ↑
          Tiempo determinado por Tarea-3 (la más lenta)
```

**Puntos clave del ejemplo:**

1. **Orden de completación != orden de envío**: Las tareas terminan según su carga, no su ID
2. **Reutilización de PIDs**: Cuando un proceso termina una tarea, toma otra de la cola
3. **Speedup real**: 2.74x con 4 cores (eficiencia ~68%)
4. **Visualización clara**: Timestamps muestran ejecución simultánea
5. **Escalabilidad**: Fácil cambiar `max_workers` para usar más/menos cores

---

#### 1.4.3 ThreadPoolExecutor vs ProcessPoolExecutor: La diferencia crucial

**Tabla comparativa:**

| Característica | `ThreadPoolExecutor` | `ProcessPoolExecutor` |
|----------------|----------------------|-----------------------|
| **Mecanismo** | Hilos (threads) | Procesos (processes) |
| **Memoria** | Compartida entre hilos | Independiente por proceso |
| **GIL** | Afecta (limita CPU-bound) | No afecta (cada proceso tiene su GIL) |
| **Overhead** | Bajo (~1-8 MB por hilo) | Alto (~10-50 MB por proceso + IPC) |
| **Startup** | Rápido (ms) | Lento (decenas de ms) |
| **Comunicación** | Variables compartidas | Serialización (pickle) |
| **Paralelismo real** | ❌ NO (solo concurrencia) | ✅ SÍ (ejecución simultánea) |
| **Usa múltiples cores** | ❌ NO efectivo (GIL) | ✅ SÍ efectivo |
| **Apropiado para** | I/O-bound | CPU-bound |

**Ejemplo visual de la diferencia:**

```python
import time
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def tarea_cpu_intensiva(n):
    """Simula trabajo CPU-bound"""
    resultado = sum(math.sqrt(i) for i in range(n))
    return resultado

def tarea_io_simulada(n):
    """Simula trabajo I/O-bound"""
    time.sleep(n)
    return f"Dormí {n} segundos"

if __name__ == "__main__":
    # Prueba 1: Tareas CPU-bound
    print("=== TAREAS CPU-BOUND ===")
    datos_cpu = [5_000_000] * 4
    
    # ThreadPoolExecutor (NO paralelo por GIL)
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(tarea_cpu_intensiva, datos_cpu))
    print(f"ThreadPool (CPU-bound): {time.time()-inicio:.2f}s")
    # Resultado típico: ~4.0s (casi secuencial)
    
    # ProcessPoolExecutor (SÍ paralelo)
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(tarea_cpu_intensiva, datos_cpu))
    print(f"ProcessPool (CPU-bound): {time.time()-inicio:.2f}s")
    # Resultado típico: ~1.2s (4x más rápido)
    
    print("\n=== TAREAS I/O-BOUND ===")
    datos_io = [1, 1, 1, 1]
    
    # ThreadPoolExecutor (SÍ concurrente, suficiente para I/O)
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(tarea_io_simulada, datos_io))
    print(f"ThreadPool (I/O-bound): {time.time()-inicio:.2f}s")
    # Resultado típico: ~1.0s (concurrencia efectiva)
    
    # ProcessPoolExecutor (también funciona, pero overhead innecesario)
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(tarea_io_simulada, datos_io))
    print(f"ProcessPool (I/O-bound): {time.time()-inicio:.2f}s")
    # Resultado típico: ~1.1s (similar, pero con overhead)
```

**Conclusión visual:**

```
CPU-BOUND (cálculos intensivos):
ThreadPoolExecutor:   ████████████████ (4s, secuencial efectivo)
ProcessPoolExecutor:  ████ (1s, paralelo real)
                      ↑
                      Speedup 4x con 4 cores

I/O-BOUND (esperas I/O):
ThreadPoolExecutor:   ████ (1s, concurrente)
ProcessPoolExecutor:  ████ (1s, paralelo pero overhead innecesario)
                      ↑
                      Ambos similares (concurrencia suficiente)
```

---

#### 1.4.4 Caso edge: Compartir datos entre procesos

**Problema:** Procesos tienen memoria independiente, no pueden compartir variables directamente.

**Ejemplo del problema:**

```python
from multiprocessing import Process

contador = 0  # Variable global

def incrementar():
    global contador
    for _ in range(1_000_000):
        contador += 1
    print(f"Contador en proceso: {contador}")

if __name__ == "__main__":
    p1 = Process(target=incrementar)
    p2 = Process(target=incrementar)
    
    p1.start(); p2.start()
    p1.join(); p2.join()
    
    print(f"Contador en main: {contador}")
    
    # Imprime:
    # Contador en proceso: 1000000
    # Contador en proceso: 1000000
    # Contador en main: 0  ← cada proceso tiene su propia copia
```

**Solución 1: Value y Array (memoria compartida)**

```python
from multiprocessing import Process, Value, Array

def incrementar(contador_compartido):
    for _ in range(1_000_000):
        with contador_compartido.get_lock():  # Lock para sincronización
            contador_compartido.value += 1

if __name__ == "__main__":
    # Crear variable compartida (tipo 'i' = int)
    contador = Value('i', 0)
    
    p1 = Process(target=incrementar, args=(contador,))
    p2 = Process(target=incrementar, args=(contador,))
    
    p1.start(); p2.start()
    p1.join(); p2.join()
    
    print(f"Contador final: {contador.value}")
    # Imprime: Contador final: 2000000 ✅
```

**Solución 2: Queue (paso de mensajes)**

```python
from multiprocessing import Process, Queue

def productor(queue, items):
    for item in items:
        queue.put(item)
        print(f"Producido: {item}")

def consumidor(queue, n):
    for _ in range(n):
        item = queue.get()
        print(f"Consumido: {item}")

if __name__ == "__main__":
    q = Queue()
    
    p1 = Process(target=productor, args=(q, [1, 2, 3, 4, 5]))
    p2 = Process(target=consumidor, args=(q, 5))
    
    p1.start(); p2.start()
    p1.join(); p2.join()
```

**Comparación con threading:**

```python
# Threading: memoria compartida natural (pero necesita locks)
import threading

contador = 0
lock = threading.Lock()

def incrementar():
    global contador
    for _ in range(1_000_000):
        with lock:
            contador += 1

# Multiprocessing: memoria separada (necesita mecanismos especiales)
from multiprocessing import Process, Value

contador = Value('i', 0)

def incrementar(cont):
    for _ in range(1_000_000):
        with cont.get_lock():
            cont.value += 1
```

**Regla:** `multiprocessing` es más complejo para compartir datos; prioriza arquitecturas donde cada proceso trabaja en datos independientes.

---

### 1.5 Casos Edge y Errores Comunes

#### 1.5.1 Async sin await: la corrutina nunca se ejecuta

```python
import asyncio

async def tarea():
    print("Esta línea NUNCA se imprime")
    return 42

# ❌ INCORRECTO
resultado = tarea()  # Solo crea el objeto coroutine
print(type(resultado))  # <class 'coroutine'>
# ⚠️ Warning: coroutine 'tarea' was never awaited

# ✅ CORRECTO
resultado = asyncio.run(tarea())
print(resultado)  # 42
```

**Regla:** Toda corrutina creada debe ser awaited (o pasada a `gather`, `create_task`, etc.).

---

#### 1.5.2 Await sin async def: error de sintaxis

```python
# ❌ ERROR
def funcion_normal():
    resultado = await alguna_corrutina()
    # SyntaxError: 'await' outside async function

# ✅ CORRECTO
async def funcion_async():
    resultado = await alguna_corrutina()
```

**Regla:** `await` solo existe dentro de `async def`.

---

#### 1.5.3 Usar time.sleep() en código async

```python
import asyncio
import time

# ❌ MAL: bloquea todo el event loop
async def mal():
    await asyncio.sleep(1)
    time.sleep(2)  # Bloquea por 2s, ninguna otra tarea puede ejecutar
    await asyncio.sleep(1)

# ✅ BIEN: permite concurrencia
async def bien():
    await asyncio.sleep(1)
    await asyncio.sleep(2)  # Libera control, otras tareas pueden ejecutar
    await asyncio.sleep(1)
```

**Regla:** En async, **nunca** uses `time.sleep()`, usa `await asyncio.sleep()`.

---

#### 1.5.4 ThreadPoolExecutor vs ProcessPoolExecutor para CPU-bound

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def cpu_heavy(n):
    return sum(range(n))

if __name__ == "__main__":
    datos = [10_000_000] * 8
    
    # ❌ MAL: ThreadPool para CPU-bound (no da paralelismo por GIL)
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(cpu_heavy, datos))
    print(f"ThreadPool: {time.time()-inicio:.2f}s")
    # Resultado: ~8s (casi secuencial)
    
    # ✅ BIEN: ProcessPool para CPU-bound (paralelismo real)
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=8) as executor:
        list(executor.map(cpu_heavy, datos))
    print(f"ProcessPool: {time.time()-inicio:.2f}s")
    # Resultado: ~1.5s (speedup ~5x con 8 cores)
```

**Regla:** Para CPU-bound, usa `ProcessPoolExecutor` (nunca `ThreadPoolExecutor`).

---

#### 1.5.5 Olvidar if __name__ == "__main__" con multiprocessing

```python
from multiprocessing import Process

def tarea():
    print("Hola")

# ❌ ERROR en Windows/macOS: crea procesos infinitos
Process(target=tarea).start()

# ✅ CORRECTO
if __name__ == "__main__":
    Process(target=tarea).start()
```

**Regla:** Siempre usa `if __name__ == "__main__"` con `multiprocessing`.

---

### 1.6 Resumen: ¿Qué herramienta usar?

**Árbol de decisión simplificado:**

```
¿Tus tareas son CPU-bound (cálculos intensivos)?
├─ Sí → ProcessPoolExecutor (paralelismo real)
│       Modelo: Sección 6 (Paralelo)
│
└─ No (I/O-bound: red, disco, DB)
    │
    ├─ ¿Tienes librerías async disponibles? (aiohttp, asyncpg, aiofiles)
    │  ├─ Sí → asyncio + gather/create_task
    │  │       Modelo: Sección 5 (Asíncrono concurrente)
    │  │
    │  └─ No → ThreadPoolExecutor
    │         Modelo: Sección 4 (Concurrente no asíncrono)
    │
    └─ ¿Una sola tarea sin paralelizar?
           → Código secuencial normal
             Modelo: Sección 2 (Secuencial)
```

**Tabla de referencia rápida:**

| Escenario | Herramienta | Ejemplo |
|-----------|-------------|---------|
| Web scraping (muchas URLs) | `asyncio` + `aiohttp` | Descargar 1000 páginas |
| Procesamiento de imágenes | `ProcessPoolExecutor` | Aplicar filtros a 100 fotos |
| Servidor web | `asyncio` + framework async | FastAPI, aiohttp |
| Cálculos científicos | `ProcessPoolExecutor` o `numpy` paralelo | Simulaciones numéricas |
| Scripts con librerías legacy | `ThreadPoolExecutor` | Usar requests (síncrono) |
| Una tarea simple | Código normal | Script que lee archivo y lo procesa |


---

**Nota final:** Este documento es pedagógico y prioriza la comprensión sobre la exhaustividad. Para uso en producción, consulta la documentación oficial de Python y considera patrones avanzados no cubiertos aquí (manejo de errores, timeouts, backpressure, etc.).

