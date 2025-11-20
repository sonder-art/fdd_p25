# Framework Matemático Formal: Modelos de Ejecución Computacional

## Glosario de Términos Fundamentales

### ¿Qué es "esperar" (wait)?

**Definición intuitiva:** Cuando una tarea está "esperando", significa que **ya inició su trabajo pero no puede continuar** hasta que ocurra algo externo. Durante este tiempo de espera, **NO se está realizando cómputo** (procesamiento activo por la CPU).

**Ejemplos concretos de espera:**

1. **Esperar I/O (Input/Output - Entrada/Salida):**
   - Leer un archivo del disco duro
   - Descargar datos de internet
   - Esperar input del usuario

2. **Esperar otros recursos:**
   - Esperar que una base de datos responda a una consulta
   - Esperar que un mutex/lock se libere
   - Esperar que un temporizador termine

**Clave:** Durante la espera, **otro proceso podría usar la CPU**. No estamos "pensando" (computando), solo aguardando que algo externo complete.

### Hilos (Threads) y Procesos

**Proceso:** Programa en ejecución con su propio espacio de memoria independiente.  
**Hilo (Thread):** Unidad de ejecución dentro de un proceso que comparte memoria con otros hilos del mismo proceso.

**Analogía:** 
- **Proceso** = Casa completa con su cocina, comedor, recursos propios
- **Hilo** = Personas dentro de la misma casa compartiendo la cocina

**Relación con Tareas (τᵢ) - Aclaración importante:**

En este documento, trabajamos con **tareas (τᵢ)** como unidad abstracta de trabajo. Una tarea NO es lo mismo que un hilo:

- **Una tarea** puede ejecutarse en un hilo, pero también puede ejecutarse en un proceso, una corrutina, o una función asíncrona
- **Un hilo** puede ejecutar múltiples tareas (alternando en el tiempo mediante)
- **Múltiples tareas** pueden compartir un solo hilo (concurrencia sin paralelismo, como en event loops)
- **Múltiples hilos** pueden ejecutar en un solo core (concurrencia sin paralelismo, mediante context switching del OS)
- **Múltiples hilos en múltiples cores** permiten paralelismo real

La distinción es crucial: las propiedades matemáticas que estudiaremos (concurrencia, asincronía, paralelismo) son independientes del mecanismo de implementación (hilos, procesos, etc.). El mismo modelo matemático puede implementarse de múltiples formas.

---

## 1. Modelo Matemático Base

### 1.1 Conjunto del Tiempo

**T** = ℝ⁺ ∪ {0}

**Interpretación:** Todos los instantes de tiempo posibles desde t=0 hasta infinito. Podemos preguntar "¿qué está pasando en el instante t=5.3 segundos?"

### 1.2 Conjunto de Tareas

**Task** = {τ₁, τ₂, ..., τₙ}

Donde:
- τ (tau) representa una tarea individual
- El subíndice i distingue las tareas: τ₁ es la primera tarea, τ₂ la segunda, etc.
- n es el número total de tareas

**Interpretación:** Cada τᵢ es una unidad de trabajo completa (ejemplo: "preparar café", "compilar programa", "enviar email").

### 1.3 Funciones Temporales para Cada Tarea

Para cada tarea τᵢ ∈ Task, definimos:

**start(τᵢ) ∈ T:** Instante de tiempo cuando τᵢ comienza  
**end(τᵢ) ∈ T:** Instante de tiempo cuando τᵢ termina completamente  
**exec(τᵢ) ⊆ T:** Conjunto de instantes donde la CPU ejecuta activamente τᵢ  
**wait(τᵢ) ⊆ T:** Conjunto de instantes donde τᵢ está esperando (sin cómputo)

### 1.4 Restricciones Fundamentales

Para cada tarea τᵢ:

1. **exec(τᵢ) ∩ wait(τᵢ) = ∅**
2. **exec(τᵢ) ∪ wait(τᵢ) = [start(τᵢ), end(τᵢ)]**

### 1.5 Notación para Instantes Específicos

Sea **t** un instante específico de tiempo (un punto en T).

**ExecutingAt(t)** = {τᵢ ∈ Task | t ∈ exec(τᵢ)}  
|ExecutingAt(t)| nos dice cuántas tareas se ejecutan simultáneamente en t.

### 1.6 Relación entre Tareas y Mecanismos de Implementación

**Abstracción vs Implementación:**

El modelo matemático trabaja con **tareas (τᵢ)** como abstracción. En la práctica, estas tareas se implementan mediante diversos mecanismos:

**Mecanismos de implementación comunes:**

Sea **Impl** = {Thread, Process, Coroutine, AsyncTask, ...} el conjunto de mecanismos de implementación.

Sea **impl: Task → Impl** una función que mapea cada tarea a su mecanismo de implementación.

**Ejemplos de mecanismos:**

1. **Thread (hilo del sistema operativo):**
   - Unidad de ejecución gestionada por el OS
   - Puede ejecutar múltiples tareas alternando (time-slicing)
   - Comparte memoria con otros threads del mismo proceso

2. **Process (proceso del sistema operativo):**
   - Programa independiente con memoria privada
   - Mayor aislamiento, mayor overhead
   - Comunicación por IPC (Inter-Process Communication)

3. **Coroutine / AsyncTask:**
   - Función que puede pausarse y reanudarse
   - Gestionada por runtime/event loop (no por OS)
   - Muy ligera, miles pueden coexistir

**Propiedad fundamental de independencia:**

Las propiedades matemáticas del sistema (concurrencia, asincronía, paralelismo) son **independientes** del mecanismo de implementación elegido.

**Ejemplo:**
- Concurrencia (∃ i≠j: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅) puede lograrse con:
  - Múltiples threads en un core (context switching)
  - Múltiples coroutines en un event loop
  - Múltiples procesos alternando

**Mapeo típico (no exclusivo):**

| Modelo | Implementación típica | Alternativas |
|--------|----------------------|--------------|
| Secuencial | 1 thread, llamadas bloqueantes | 1 proceso |
| Asínc. no conc. | 1 thread, event loop ocioso | 1 coroutine sin scheduler |
| Conc. no asínc. | N threads en 1 core | N procesos en 1 core |
| Asínc. conc. | 1 thread + event loop, N coroutines | Thread pool pequeño |
| Paralelo | N threads en N cores | N procesos en N cores |
| Distribuido | N procesos en N nodos | N containers, N VMs |

**Notación en el resto del documento:**

Cuando escribimos "tarea τᵢ", nos referimos a la abstracción matemática. Las secciones posteriores incluirán subsecciones sobre implementaciones concretas para conectar teoría con práctica.

---

## 2. SECUENCIAL

### 2.1 Definición Matemática Formal

Un sistema es **secuencial** si y solo si:

**∀ τᵢ, τⱼ ∈ Task, i ≠ j:** (end(τᵢ) ≤ start(τⱼ)) **OR** (end(τⱼ) ≤ start(τᵢ))

Interpretación: Para cualquier par de tareas diferentes, una debe terminar completamente antes de que la otra comience.

Propiedades derivadas:
- **|ExecutingAt(t)| = 1** para todo t con ejecución
- Las tareas forman una secuencia totalmente ordenada: τ₁ → τ₂ → τ₃ → …
- No hay solapamiento temporal entre intervalos [start(τᵢ), end(τᵢ)]

### 1.7 Analogía base que usaremos en todo el documento

Usaremos la analogía de una cocina profesional:

**Elementos físicos (hardware):**
- **Núcleo de CPU (core)**: un chef humano. Un chef solo puede hacer una acción fina a la vez.
- **Procesador con P núcleos**: una brigada con P chefs que pueden trabajar físicamente en paralelo.

**Elementos de organización (software):**
- **Proceso**: una cocina independiente con su propia despensa y utensilios (memoria privada). Dos procesos no comparten despensa.
- **Hilo (thread)**: un cocinero/ayudante perteneciente a la misma cocina (proceso) que comparte la misma despensa y utensilios (memoria compartida). Si hay un solo chef (P=1), los hilos alternan turnos sobre el mismo chef.

**Abstracción matemática (modelo):**
- **Tarea τᵢ**: una orden concreta (preparar café, tostar pan, leer periódico). Es una unidad de trabajo completa (abstracción).
- **exec(τᵢ)**: el chef está manipulando activamente esa orden (cortando, mezclando, sirviendo).
- **wait(τᵢ)**: la orden está "en manos" de un dispositivo/condición externa (horno, tostadora, cafetera, temporizador, red); el chef no realiza cómputo.

**Mecanismos de control:**
- **Planificador (scheduler)**: el jefe de cocina que decide a qué orden le dedica el chef su siguiente turno.
- **Mapeo task→thread (impl)**: el jefe de cocina decide QUÉ cocinero ejecuta QUÉ orden.

**Relación entre tarea, hilo y chef:**
- Una **tarea (τᵢ)** es la orden abstracta: "preparar café"
- Un **hilo (thread)** es el cocinero asignado a ejecutar órdenes
- Un **chef (core)** es quien físicamente realiza el trabajo
- El **mapeo**: tarea → hilo → chef

Ejemplo: τ₁ (preparar café) puede ser ejecutada por hilo h₁ (cocinero Juan), que a su vez usa chef c₁ (Chef principal). Si hay P=1 chef y H=3 hilos (Juan, María, Pedro), los tres cocineros se turnan para usar al único chef disponible.

**Invariante clave de la analogía:** 
Con P=1, aunque haya muchos hilos/órdenes, el chef solo puede ejecutar una acción a la vez; el resto está en espera de turno o en espera externa (wait).

**Aclaración fundamental:**
En este documento, cuando decimos "tarea τᵢ" nos referimos a la unidad de trabajo abstracta (la orden). En la práctica, esta tarea puede ejecutarse mediante un hilo, un proceso, una corrutina, o una función asíncrona. La elección del mecanismo NO cambia las propiedades matemáticas (concurrencia, asincronía, paralelismo) que estamos estudiando.

---

### 2.2 Analogía (basada en la cocina)

Un solo chef atiende una lista de órdenes y completa cada una por completo antes de tomar la siguiente; nunca inicia otra mientras no termine la actual.

### 2.3 Diagrama de Gantt - Secuencial (simplificado)

```
τ₁ (moler)     [██████]
τ₂ (hervir)            [████████]
τ₃ (café)                       [██████████]
τ₄ (tostar)                                [████]
τ₅ (huevos)                                     [████████]

Leyenda: █ = ejecución activa
```

Notas (secuencial):
- No se muestra eje temporal para evitar desalineaciones visuales; el orden y no el tiempo exacto es lo relevante aquí.
- No existen wait states solapados con otras tareas (no aplica).

### 2.4 Implementación típica: un solo hilo, ejecución bloqueante

**Mecanismo de implementación:**

- **Hilos**: H = 1 (un solo hilo)
- **Cores**: P = 1 (un solo core, aunque podría ser P > 1 sin aprovecharse)
- **Mapeo**: impl(τᵢ) = thread_main para toda τᵢ
- **Scheduler**: no necesario; las tareas se llaman secuencialmente de forma bloqueante

**Características:**

1. Todas las tareas se ejecutan en el mismo hilo (típicamente el hilo principal del programa)
2. Cada llamada a función es **bloqueante**: la función no retorna hasta completar toda su ejecución
3. No hay scheduler del OS involucrado (no hay context switching)
4. Si una tarea entra en wait (ej: esperar I/O), el hilo se bloquea completamente

**Formalización:**

Sea thread_main el único hilo del sistema.

∀ τᵢ ∈ Task: impl(τᵢ) = thread_main

La ejecución es estrictamente secuencial: τ₁ completa → τ₂ inicia → τ₂ completa → τ₃ inicia → ...

**Ejemplos de lenguajes/contextos:**
- Script Python simple sin threading ni asyncio
- Programa C sin pthreads
- JavaScript síncrono (sin async/await, sin callbacks)
- Cualquier programa que solo use llamadas bloqueantes

**Ventajas:**
- Simplicidad máxima: fácil de entender y debuggear
- Sin overhead de context switching
- Sin problemas de race conditions

**Desventajas:**
- No aprovecha múltiples cores (si P > 1)
- No aprovecha wait times (CPU ociosa durante I/O)
- Tiempo total = suma de todos los tiempos individuales

---

## 3. ASÍNCRONO Y NO CONCURRENTE (SIN PARALELISMO)

### 3.1 Definición Matemática Formal

Un sistema es **asíncrono y no concurrente** si:

1. Concurrencia ausente (no hay solapamiento de vidas de tareas):  
   **∀ τᵢ, τⱼ ∈ Task, i ≠ j:** [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] = ∅

2. Asincronía presente (existen períodos de espera reales):  
   **∃ τₖ ∈ Task:** wait(τₖ) ≠ ∅

3. No se aprovechan los períodos de espera (CPU ociosa durante waits):  
   Forma equivalente A (por instantes): **∀ t ∈ T**, si ∃ τᵢ con t ∈ wait(τᵢ) ⇒ |ExecutingAt(t)| = 0  
   Forma equivalente B (por conjuntos): **∀ i, j:** exec(τⱼ) ∩ wait(τᵢ) = ∅

4. Número de procesadores: **P = 1** (sin paralelismo físico)
Tecnicamente podria existir paralelimso y ser concurrente no asincrono, pero decidimos no hacerlo paralelo para entender cada concepto de manera aislada.  
No es necesario este supuesto para ser Concurrente no Asíncrono, pero al ponerlo se hace no paralelo.  

Propiedades derivadas:
- |ExecutingAt(t)| ∈ {0, 1}; hay intervalos con CPU ociosa.
- Es “casi secuencial”, pero con tiempos muertos debidos a waits.
- El tiempo total es mayor que en el caso asíncrono concurrente (donde se aprovecharían los waits).

### 3.2 Analogía (basada en la cocina)

El chef inicia una cafetera y, durante el goteo (wait), decide no avanzar ninguna otra orden: se queda mirando. Más tarde inicia la tostadora y, durante el tostado (wait), tampoco avanza otra orden. Finalmente, cuando todos los dispositivos han terminado, retoma acciones activas. Hay esperas reales, pero no se aprovechan para ejecutar otras tareas: no hay concurrencia.

### 3.3 Diagrama - Asíncrono y No Concurrente (CPU ociosa en waits)

```
CPU:   [τ₁]  IDLE...........  [τ₂]  IDLE......  [τ₂]  [τ₃....]

τ₁:    [█]░░░░░░░░░░░░░░░░░░░[█]          (WAIT central no aprovechado)
τ₂:                             [█]░░░░[█]    (WAIT central no aprovechado)
τ₃:                                       [██████]

Leyenda:
  █ = ejecución activa (CPU)
  ░ = espera (dispositivo/temporizador); la CPU está ociosa
```

### 3.4 Tabla de análisis temporal (conceptual)

| Intervalo conceptual | CPU ejecuta | τ₁ estado | τ₂ estado | τ₃ estado |
|----------------------|-------------|-----------|-----------|-----------|
| I                    | τ₁ (exec)   | EXEC      | —         | —         |
| II                   | IDLE        | WAIT      | —         | —         |
| III                  | τ₁ (exec)   | EXEC      | —         | —         |
| IV                   | τ₂ (exec)   | Completa  | EXEC      | —         |
| V                    | IDLE        | Completa  | WAIT      | —         |
| VI                   | τ₂ (exec)   | Completa  | EXEC      | —         |
| VII                  | τ₃ (exec)   | Completa  | Completa  | EXEC      |

Notas:
- Los “intervalos” I..VII son etiquetas conceptuales (no tiempo absoluto).
- No hay solapamiento de vidas de tareas; hay esperas reales no aprovechadas.

### 3.5 Diferencias respecto a “asíncrono y concurrente” (sin paralelismo)

- Concurrencia:  
  - Asíncrono concurrente: ∃ i≠j: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅  
  - Asíncrono NO concurrente: ∀ i≠j: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] = ∅
- Aprovechamiento de waits:  
  - Asíncrono concurrente: ∃ i,j: exec(τⱼ) ∩ wait(τᵢ) ≠ ∅  
  - Asíncrono NO concurrente: ∀ i,j: exec(τⱼ) ∩ wait(τᵢ) = ∅
- Ambos con P=1 (sin paralelismo físico).

### 3.6 Implementación típica: un hilo con event loop ocioso

**Mecanismo de implementación:**

- **Hilos**: H = 1 (un solo hilo)
- **Cores**: P = 1
- **Mapeo**: impl(τᵢ) = thread_main para toda τᵢ
- **Scheduler**: event loop presente pero NO registra callbacks para otras tareas durante waits

**Características:**

1. Hay un event loop o runtime asíncrono, pero configurado para NO aprovechar los waits
2. Cuando una tarea entra en wait, el event loop queda ocioso (no ejecuta otras tareas)
3. Las tareas se ejecutan secuencialmente, pero con capacidad de entrar en estados wait
4. Es "casi secuencial" pero con tiempos muertos

**Formalización:**

Sea thread_main el único hilo con event loop.

∀ τᵢ ∈ Task: impl(τᵢ) = thread_main

Cuando τᵢ entra en wait, el event loop NO selecciona otra tarea para ejecutar.

**Ejemplos de lenguajes/contextos:**
- Python asyncio con tareas ejecutadas secuencialmente (await sin gather)
- JavaScript con async/await pero sin Promise.all
- Event loop con una sola tarea registrada a la vez

**Por qué existe este patrón:**
- Simplicidad: se usa async/await para manejar I/O, pero sin la complejidad de concurrencia
- Debugging: más fácil de debuggear que concurrencia completa
- Transición: paso intermedio al migrar de código síncrono a asíncrono

**Desventajas:**
- No aprovecha los wait times (peor rendimiento que asíncrono concurrente)
- Tiempo total mayor que si se aprovecharan los waits

---

## 4. CONCURRENTE NO ASÍNCRONO (SIN PARALELISMO)

### 4.1 Definición Matemática Formal

Un sistema es **concurrente no asíncrono** si:

1. Hay concurrencia (solapamiento de vidas de tareas):  
   **∃ τᵢ, τⱼ ∈ Task, i ≠ j:** [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅

2. No hay asincronía (todas las tareas son CPU-bound):  
   **∀ τₖ ∈ Task:** wait(τₖ) = ∅

3. No hay ejecución simultánea física (P=1):  
   **∀ i≠j:** exec(τᵢ) ∩ exec(τⱼ) = ∅
Tecnicamente podria existir paralelimso y ser concurrente no asincrono, pero decidimos no hacerlo paralelo para entender cada concepto de manera aislada.  
No es necesario este supuesto para ser Concurrente no Asíncrono, pero al ponerlo se hace no paralelo.  

4. Mecanismo: división del tiempo (time-slicing) con quantum q > 0.

Propiedades:
- **|ExecutingAt(t)| = 1** para todo t con ejecución
- Alternancia rápida entre tareas (cambios de contexto)
- Las tareas avanzan “simultáneamente” a nivel estructural, no físicamente

### 4.2 Analogía (basada en la cocina)

Tres órdenes requieren atención constante (no esperan dispositivos): el chef revuelve un risotto 20s, cambia a batir una salsa 20s, cambia a saltear vegetales 20s, y repite el ciclo. No hay “esperas externas”; las pausas entre bloques de una misma orden son simplemente turnos de CPU reasignados a otra orden.

### 4.3 Diagrama - Concurrente No Asíncrono (time-slicing, P=1)

```
τ₁:  [██       ██       ██]
τ₂:     [██       ██       ██]
τ₃:        [██       ██       ██]
Si esta vacio no hay ejecucion ni espera.
Leyenda:
  Cada bloque [██] representa un quantum de CPU dedicado a la MISMA tarea.
  Entre bloques de una misma tarea NO hay WAIT (la tarea está pausada, lista).
```

### 4.4 Tabla de análisis (conceptual con quantum q)

| Turno | CPU ejecuta | τ₁ | τ₂ | τ₃ |
|-------|-------------|----|----|----|
| 1     | τ₁          | EXEC | LISTA | LISTA |
| 2     | τ₂          | LISTA | EXEC | LISTA |
| 3     | τ₃          | LISTA | LISTA | EXEC |
| 4     | τ₁          | EXEC | LISTA | LISTA |
| 5     | τ₂          | LISTA | EXEC | LISTA |
| 6     | τ₃          | LISTA | LISTA | EXEC |

Notas:
- “LISTA” significa pausada esperando su próximo turno de CPU (no es WAIT).
- No hay espera por I/O/temporizador; todas requieren CPU continua.

### 4.5 Diferencias con el caso asíncrono (sin paralelismo)

- Esperas (wait):  
  - Concurrente no asíncrono: wait(τ)=∅  
  - Asíncrono (concurrente o no): ∃ τ con wait(τ)≠∅
- Paralelismo: en ambos casos P=1, no hay ejecución simultánea física.
- Estructura temporal:  
  - Concurrente no asíncrono: avances por time-slicing (pausas activas, “LISTA”)  
  - Asíncrono: alternancia impulsada por waits reales (I/O, timers, etc.)

### 4.6 Cambio de tarea: sin espera vs por espera (explicación clara)

- Concurrente no asíncrono (sin waits):
  - ¿Por qué cambia la CPU de tarea? Porque se acabó el “turno” (quantum) o por decisión del planificador, aunque la tarea todavía podía seguir trabajando.
  - ¿Qué pasa con la CPU? Si hay alguna tarea LISTA, la CPU nunca queda ociosa (siempre hay alguien a quien darle el turno).

- Asíncrono no concurrente (hay waits, pero no se aprovechan):
  - ¿Por qué se detiene la tarea? Porque entra a una ESPERA real (I/O, temporizador, bloqueo de recurso).
  - ¿Se ejecuta otra tarea durante esa espera? No. El planificador NO toma otra tarea.
  - ¿Qué pasa con la CPU? La CPU queda OCIOSA durante la espera.
  - Consecuencia: No hay solapamiento de vidas de tareas; por eso no hay concurrencia.

Nota aclaratoria: Si, en el caso asíncrono, al entrar una tarea en ESPERA la CPU tomara otra tarea LISTA y la ejecutara, entonces habría solapamiento de vidas y el sistema sería "asíncrono y concurrente" (aunque siempre con P=1, sin paralelismo físico).

### 4.7 Implementación típica: múltiples hilos con time-slicing en P=1

**Mecanismo de implementación:**

- **Hilos**: H ≥ 2 (múltiples hilos, típicamente H > P)
- **Cores**: P = 1 (un solo core)
- **Mapeo**: impl(τᵢ) puede ser thread_1, thread_2, ..., thread_H
- **Scheduler**: scheduler del OS realiza context switching con quantum q

**Características:**

1. Múltiples hilos del sistema operativo (OS threads)
2. Todos los hilos comparten el mismo core (P=1)
3. El scheduler del OS alterna entre hilos cada quantum q (típicamente 10-100ms)
4. Todas las tareas son CPU-bound (no hay waits reales, o los waits son muy cortos)

**Formalización:**

Sea H = {h₁, h₂, ..., hₙ} el conjunto de hilos.

Sea thread: Task → H la función que asigna tareas a hilos.

Con P=1, en cada instante t, solo un hilo ejecuta: |{h ∈ H | h ejecuta en t}| = 1

El scheduler del OS decide qué hilo ejecuta en cada quantum.

**Ejemplos de lenguajes/contextos:**
- Python threading con tareas CPU-bound en una máquina con 1 core
- Java threads en un procesador single-core
- Pthreads en C con P=1
- Cualquier programa multi-threaded en hardware con un solo core

**Ventajas:**
- Permite estructura de código modular (cada hilo maneja una responsabilidad)
- El OS maneja el scheduling automáticamente
- Útil para separar concerns (UI thread vs worker thread)

**Desventajas:**
- Overhead de context switching (guardar/restaurar estado de registros, caché)
- No hay speedup real (tiempo total similar o peor que secuencial)
- Complejidad: race conditions, deadlocks, necesidad de sincronización
- En Python: GIL (Global Interpreter Lock) limita aún más

**Nota importante:**
Este patrón es común en sistemas embebidos o legacy con un solo core, o en lenguajes con limitaciones (como Python con GIL) donde threading no da paralelismo real.

---


## 5. CONCURRENTE Y ASÍNCRONO (SIN PARALELISMO)

### 5.1 Definición Matemática Formal

Un sistema es **concurrente y asíncrono** si:

1. Concurrencia (solapamiento de vidas de tareas):  
   **∃ τᵢ, τⱼ ∈ Task, i ≠ j:** [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅

2. Asincronía (existen períodos de espera reales):  
   **∃ τₖ ∈ Task:** wait(τₖ) ≠ ∅

3. Sin ejecución simultánea física (P=1, sin paralelismo):  
   **∀ i≠j:** exec(τᵢ) ∩ exec(τⱼ) = ∅
Tecnicamente podria existir paralelimso y ser concurrente no asincrono, pero decidimos no hacerlo paralelo para entender cada concepto de manera aislada.  
No es necesario este supuesto para ser Concurrente no Asíncrono, pero al ponerlo se hace no paralelo.  

4. Consecuencia característica (aprovechamiento de esperas):  
**∃ i, j:** exec(τⱼ) ∩ wait(τᵢ) ≠ ∅  
Interpretación: mientras una tarea espera (wait), la CPU ejecuta otra.

Propiedades derivadas:
- **|ExecutingAt(t)| ≤ 1**; la CPU ejecuta a lo más una tarea a la vez.
- Si todas las tareas activas están en WAIT, la CPU queda ociosa.
- Cuando hay al menos una tarea lista para ejecutar, se aprovechan los WAIT de otras para avanzar.

### 5.2 Analogía (basada en la cocina)

El chef inicia la cafetera (espera larga) y la tostadora (espera corta). Mientras ambos “dispositivos” trabajan solos, el chef corta fruta (trabajo continuo). Cuando la tostadora o la cafetera “piden” atención, el chef hace intervenciones breves (meter/sacar pan, servir café) y regresa a cortar fruta. Se aprovechan los tiempos de espera para avanzar otras órdenes: hay concurrencia, sin paralelismo (un solo chef).

### 5.3 Diagrama - Concurrente y Asíncrono (P=1, aprovecha WAIT)

```
Vista de CPU (quién ejecuta en cada momento):
CPU:              [τ₁][τ₂][τ₃...........][τ₂][τ₃.]   [τ₁]
τ₁ (cafetera):    [█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█]
τ₂ (tostadora):       [█░░░░░░░░░░░░░░░███]
τ₃ (cortar fruta):        [████████████      ████]

Leyenda:
  █ = ejecución activa (usando CPU)
  ░ = espera (dispositivo/temporizador) o pausada (cedió CPU)
  vacio = no hay ejecución activa ni espera (como en cortar fruta)
Lectura vertical (alineación por columnas):
- Inicio: τ₁ ejecuta brevemente, luego entra a WAIT largo (cafetera goteando).
- τ₂ ejecuta brevemente, entra a WAIT (pan tostándose).
- Mientras τ₁ y τ₂ esperan, τ₃ toma la CPU y ejecuta trabajo continuo.
- Cuando τ₂ necesita atención (pan listo), interrumpe a τ₃ brevemente.
- τ₃ retoma y continúa hasta que τ₁ necesita atención final (servir café).
- Solapamiento temporal: las tres tareas tienen vidas [start, end] que se cruzan.
```

### 5.4 Tabla de análisis temporal (conceptual)

| Intervalo | CPU ejecuta | τ₁ estado | τ₂ estado | τ₃ estado |
|-----------|-------------|-----------|-----------|-----------|
| I         | τ₁ (exec)   | EXEC      | —         | —         |
| II        | τ₂ (exec)   | WAIT      | EXEC      | —         |
| III       | τ₃ (exec)   | WAIT      | WAIT      | EXEC      |
| IV        | τ₂ (exec)   | WAIT      | EXEC      | PAUSADA   |
| V         | τ₃ (exec)   | WAIT      | COMPLETA  | EXEC      |
| VI        | τ₁ (exec)   | EXEC      | COMPLETA  | PAUSADA   |

Notas:
- En III y V, τ₃ avanza mientras τ₁ y/o τ₂ están en WAIT.
- “PAUSADA” indica que τ₃ se detiene solo para ceder CPU brevemente (no es WAIT).

### 5.5 Propiedades clave

- Aprovechamiento de esperas: aumenta el rendimiento respecto al asíncrono no concurrente (sección 3).
- Sin paralelismo: nunca hay dos ejecuciones simultáneas; la mejora proviene de alternancia inteligente.
- CPU ociosa solo cuando todas las tareas activas están en WAIT a la vez.

### 5.6 Diferencias con secciones 3 y 4

- Vs 3 (Asíncrono y NO concurrente):
  - 3: ∀ i,j: exec(τⱼ) ∩ wait(τᵢ) = ∅ (no se aprovecha el WAIT; CPU ociosa).
  - 5: ∃ i,j: exec(τⱼ) ∩ wait(τᵢ) ≠ ∅ (sí se aprovecha el WAIT; CPU ocupada).
  - Ambos con P=1 y hay waits; difieren en si se solapan vidas de tareas.

- Vs 4 (Concurrente NO asíncrono):
  - 4: ∀ τ: wait(τ)=∅ (no hay esperas reales); alternancia por quantum (LISTA).
  - 5: ∃ τ: wait(τ)≠∅ (sí hay esperas); alternancia inducida por WAIT y por planificación.
  - Ambos con P=1 y concurrencia; difieren en la existencia de WAIT reales.

### 5.7 Implementación típica: event loop con múltiples tareas o thread pool pequeño

**Mecanismo de implementación (Opción A - Event loop):**

- **Hilos**: H = 1 (un solo hilo)
- **Cores**: P = 1
- **Mapeo**: todas las tareas τᵢ se ejecutan en thread_main, pero alternando
- **Scheduler**: event loop con cola de tareas listas y callbacks registrados

**Mecanismo de implementación (Opción B - Thread pool pequeño):**

- **Hilos**: H = pequeño número (ej: 2-4 hilos)
- **Cores**: P = 1
- **Mapeo**: impl(τᵢ) puede variar, pero con H > P hay time-slicing
- **Scheduler**: combinación de event loop + scheduler del OS

**Características (Opción A - más común):**

1. Un solo hilo con event loop (ej: Python asyncio, JavaScript, Node.js)
2. Múltiples tareas (coroutines/promises) registradas en el event loop
3. Cuando una tarea entra en wait, el event loop selecciona otra tarea lista
4. No hay paralelismo físico, pero sí aprovechamiento de waits

**Formalización (Opción A):**

Sea thread_main el hilo con event loop.

Sea TaskQueue la cola de tareas listas para ejecutar.

∀ τᵢ ∈ Task: impl(τᵢ) = coroutine ejecutada en thread_main

Cuando τᵢ entra en wait:
1. Se registra callback para cuando termine el wait
2. Event loop selecciona τⱼ ∈ TaskQueue
3. Ejecuta τⱼ hasta que entre en wait o complete

**Ejemplos de lenguajes/contextos:**
- Python asyncio con asyncio.gather() (múltiples coroutines)
- JavaScript con async/await + Promise.all()
- Node.js (event loop nativo)
- Go con goroutines (modelo M:N, pero conceptualmente similar)
- Rust con async/await + tokio

**Ventajas:**
- Máximo aprovechamiento de CPU en P=1
- Muy eficiente para tareas I/O-bound
- Bajo overhead (sin context switching de OS)
- Miles de tareas concurrentes posibles

**Desventajas:**
- No aprovecha múltiples cores (si P > 1, se desperdician)
- Requiere código asíncrono (async/await, callbacks)
- Debugging más complejo que secuencial
- Si una tarea bloquea el event loop, todo se detiene

**Cuándo usar:**
- Servidores web con muchas conexiones simultáneas
- Aplicaciones I/O-bound (red, disco, DB)
- Cuando P=1 o cuando las tareas son mayormente wait

---

## 6. PARALELO

### 6.1 Definición Matemática Formal

Un sistema es **paralelo** si:

1. Existe ejecución simultánea física (en el mismo instante):  
   **∃ τᵢ, τⱼ ∈ Task, i ≠ j, ∃ t ∈ T:** (t ∈ exec(τᵢ)) **AND** (t ∈ exec(τⱼ))

   Interpretación: Existe al menos un instante t donde dos tareas diferentes se ejecutan simultáneamente en la CPU.

2. Número de procesadores:  
   **P ≥ 2** (mínimo dos núcleos/cores físicos)

3. Cardinalidad de ejecución simultánea:  
   **∃ t ∈ T:** |ExecutingAt(t)| ≥ 2

   Interpretación: En algún momento, al menos dos tareas ejecutan al mismo tiempo.

Propiedades derivadas:
- Paralelismo ⊆ Concurrencia (todo sistema paralelo es concurrente, pero no viceversa)
- **exec(τᵢ) ∩ exec(τⱼ) ≠ ∅** para al menos un par de tareas
- Puede haber asincronía (waits) o no; el paralelismo es ortogonal a la asincronía
- Speedup potencial: hasta P veces más rápido que secuencial (en condiciones ideales)

Nota importante sobre hilos:
- "Múltiples hilos" NO garantiza paralelismo automáticamente
- Si H hilos y P cores, con H > P, entonces algunos hilos comparten cores (no todos son paralelos)
- Ejemplo: 10 hilos en P=1 → concurrente no paralelo; 10 hilos en P=4 → máximo 4 paralelos simultáneamente

### 6.2 Analogía (basada en la cocina)

Ahora tenemos P=2 chefs trabajando simultáneamente en la misma cocina (o cocinas separadas). El Chef A prepara un risotto (requiere revolver constantemente durante 15 minutos) mientras el Chef B prepara una salsa (requiere batir constantemente durante 15 minutos). Ambos trabajan al mismo tiempo físicamente: en t=7 minutos, Chef A está revolviendo Y Chef B está batiendo. Esto es paralelismo real.

Diferencia clave con P=1: con un solo chef, nunca hay dos acciones simultáneas; con P≥2, sí puede haber ejecución física simultánea.

### 6.3 Diagrama - Paralelo (P=2, ejecución simultánea física)

```
Vista por procesador (cada chef trabaja independientemente):
CPU_A:            [████████████████ τ₁ ████████████████]
CPU_B:            [████████████████ τ₂ ████████████████]

Vista por tarea:
τ₁ (risotto):     [████████████████████████████████████]
τ₂ (salsa):       [████████████████████████████████████]

Leyenda:
  █ = ejecución activa
  
Lectura:
- Durante todo el intervalo, CPU_A ejecuta τ₁ y CPU_B ejecuta τ₂ simultáneamente.
- En cualquier instante t dentro del intervalo: |ExecutingAt(t)| = 2
- exec(τ₁) ∩ exec(τ₂) = intervalo completo ≠ ∅ (ejecución simultánea física)
```

### 6.4 Tabla de análisis temporal (P=2)

| Intervalo | CPU_A ejecuta | CPU_B ejecuta | |ExecutingAt(t)| |
|-----------|---------------|---------------|------------------|
| Completo  | τ₁ (risotto)  | τ₂ (salsa)    | 2                |

Notas:
- Ambas tareas ejecutan en paralelo durante todo su ciclo de vida.
- No hay alternancia ni time-slicing entre τ₁ y τ₂; cada una tiene su propio core.
- Si hubiera una tercera tarea τ₃ con solo P=2, entonces τ₃ esperaría o se alternaría con τ₁ o τ₂.

### 6.5 Propiedades clave del paralelismo

- **Speedup real**: con P cores y N tareas CPU-bound independientes (N ≤ P), el tiempo total puede reducirse hasta P veces respecto a secuencial.
- **Overhead**: comunicación/sincronización entre cores puede reducir el speedup ideal.
- **Ley de Amdahl**: si una fracción del trabajo es inherentemente secuencial, el speedup máximo está limitado.
- **Paralelismo + asincronía**: es posible tener P>1 y también waits; por ejemplo, P=2 con tareas que hacen I/O.

### 6.6 Diferencias con secciones anteriores (todas con P=1)

- Vs secciones 2, 3, 4, 5 (todas con P=1):
  - Secciones 2-5: ∀ i≠j: exec(τᵢ) ∩ exec(τⱼ) = ∅ (nunca ejecución simultánea física)
  - Sección 6: ∃ i≠j: exec(τᵢ) ∩ exec(τⱼ) ≠ ∅ (sí hay ejecución simultánea física)
  - Secciones 2-5: |ExecutingAt(t)| ≤ 1 siempre
  - Sección 6: ∃ t con |ExecutingAt(t)| ≥ 2

- Paralelismo es independiente de asincronía:
  - Puede haber paralelismo sin waits (P=2, tareas CPU-bound)
  - Puede haber paralelismo con waits (P=2, tareas con I/O)

### 6.7 Composición: paralelismo con concurrencia/asincronía interna

Nota importante: cada procesador (core) puede, a su vez, manejar múltiples tareas de forma concurrente o asíncrona.

**Ejemplo con P=2:**
- CPU_A ejecuta τ₁, τ₂, τ₃ de forma concurrente (time-slicing interno en ese core)
- CPU_B ejecuta τ₄, τ₅ de forma asíncrona y concurrente (aprovechando waits internos)
- A nivel global: hay paralelismo (CPU_A y CPU_B trabajan simultáneamente)
- A nivel local (dentro de cada core): hay concurrencia/asincronía

**Formalización:**
- Sea Taskₐ el conjunto de tareas asignadas a CPU_A
- Sea Task_b el conjunto de tareas asignadas a CPU_B
- Paralelismo entre cores: ∃ τᵢ ∈ Taskₐ, τⱼ ∈ Task_b, ∃ t: (t ∈ exec(τᵢ)) AND (t ∈ exec(τⱼ))
- Concurrencia dentro de CPU_A: ∃ τₖ, τₘ ∈ Taskₐ: [start(τₖ), end(τₖ)] ∩ [start(τₘ), end(τₘ)] ≠ ∅
- Asincronía dentro de CPU_A: ∃ τₙ ∈ Taskₐ: wait(τₙ) ≠ ∅

**Analogía de la cocina:**
- Chef A (CPU_A) maneja 3 órdenes alternando entre ellas (concurrencia interna)
- Chef B (CPU_B) maneja 2 órdenes aprovechando esperas de dispositivos (asincronía interna)
- Ambos chefs trabajan simultáneamente (paralelismo entre chefs)

Esto permite sistemas híbridos muy eficientes: P cores trabajando en paralelo, cada uno manejando N tareas de forma concurrente/asíncrona.

### 6.8 Implementación típica: mapeo de hilos/procesos a cores

**Mecanismo de implementación:**

- **Hilos**: H ≥ P (al menos tantos hilos como cores para paralelismo real)
- **Cores**: P ≥ 2 (múltiples cores físicos)
- **Mapeo**: impl(τᵢ) → thread_j → core_k (cada tarea a un hilo, cada hilo a un core)
- **Scheduler**: scheduler del OS asigna hilos a cores; idealmente H ≤ P para evitar time-slicing

**Características:**

1. Múltiples hilos del OS o procesos independientes
2. Cada core puede ejecutar un hilo simultáneamente
3. Si H ≤ P: cada hilo tiene su core dedicado (paralelismo puro)
4. Si H > P: algunos hilos comparten cores (paralelismo parcial + concurrencia)

**Formalización:**

Sea H = {h₁, h₂, ..., hₙ} el conjunto de hilos.

Sea C = {c₁, c₂, ..., cₚ} el conjunto de cores.

Sea assign: H → C la función de asignación de hilos a cores (gestionada por OS).

Paralelismo real ocurre cuando: ∃ t, ∃ hᵢ, hⱼ: (assign(hᵢ) ≠ assign(hⱼ)) AND (ambos ejecutan en t)

**Ejemplos de lenguajes/contextos:**
- Python multiprocessing (evita GIL, usa procesos)
- Java threads en máquina multi-core
- C/C++ con pthreads o std::thread
- Go goroutines con GOMAXPROCS > 1
- Rust threads nativos

**Dos enfoques principales:**

1. **Threads (hilos):**
   - Comparten memoria (más rápido para comunicación)
   - Menor overhead de creación
   - Riesgo de race conditions
   - En Python: limitado por GIL

2. **Processes (procesos):**
   - Memoria independiente (más seguro, más aislamiento)
   - Mayor overhead de creación y comunicación (IPC)
   - Sin race conditions entre procesos
   - En Python: multiprocessing evita GIL

**Ventajas:**
- Speedup real: hasta P veces más rápido (en tareas CPU-bound)
- Aprovecha hardware moderno (todos los cores)
- Ideal para tareas CPU-bound (cálculos, procesamiento)

**Desventajas:**
- Mayor complejidad: sincronización, race conditions
- Overhead de comunicación entre cores (caché coherence)
- No siempre da speedup lineal (Ley de Amdahl)
- Debugging más difícil

**Cuándo usar:**
- Tareas CPU-bound (cálculos matemáticos, procesamiento de imágenes)
- Cuando P > 1 y las tareas son independientes o requieren poca sincronización
- Machine learning, renderizado, compilación paralela

---

## 7. DISTRIBUIDO

### 7.1 Definición Matemática Formal

Sea **N** = {n₁, n₂, ..., nₘ} un conjunto de nodos computacionales (máquinas/servidores físicamente separados).

Sea **location: Task → N** una función que asigna cada tarea a un nodo específico.

Sea **δᵢⱼ: N × N → ℝ⁺** una función de latencia de red entre nodos i y j.

Un sistema es **distribuido** si:

1. Múltiples nodos físicamente separados:  
   **|N| ≥ 2**

2. Existe latencia de comunicación entre nodos:  
   **∀ nᵢ, nⱼ ∈ N, i ≠ j: δᵢⱼ > 0**
   
   Interpretación: Comunicarse entre nodos toma tiempo (milisegundos a segundos); no es instantáneo.

3. Tareas ejecutan en nodos diferentes:  
   **∃ τᵢ, τⱼ ∈ Task:** location(τᵢ) ≠ location(τⱼ)

4. Separación física significativa:  
   **∀ nᵢ, nⱼ ∈ N, i ≠ j:** distance(nᵢ, nⱼ) ≥ d_min
   
   Interpretación: Los nodos están físicamente distantes (típicamente > 1 metro, usualmente kilómetros).

5. No hay memoria compartida global:  
   Cada nodo tiene su propia RAM; la comunicación es por paso de mensajes (red).

Propiedades derivadas:
- **Distribuido ⊂ Paralelo ⊂ Concurrente** (jerarquía de inclusión)
- Posibilidad de fallos parciales independientes (un nodo puede fallar sin afectar a otros)
- Comunicación mediante paso de mensajes con latencia δᵢⱼ
- Cada nodo puede tener P ≥ 1 cores locales
- Desafíos adicionales: sincronización, consistencia, tolerancia a fallos, particiones de red

### 7.2 Analogía (basada en la cocina)

Ahora tenemos N=3 restaurantes en ciudades diferentes:
- Restaurante en CDMX (nodo n₁) con su propia cocina y chefs
- Restaurante en Guadalajara (nodo n₂) con su propia cocina y chefs
- Restaurante en Monterrey (nodo n₃) con su propia cocina y chefs

Tarea distribuida: preparar un banquete de 300 personas en Querétaro.

Subtareas:
- τ₁: n₁ (CDMX) prepara 100 platos principales
- τ₂: n₂ (GDL) prepara 100 ensaladas
- τ₃: n₃ (MTY) prepara 100 postres

Propiedades clave:
- Separación física: cientos de kilómetros entre restaurantes
- Latencia de comunicación: llamadas telefónicas/mensajes tardan segundos; transporte físico tarda horas
- Sin memoria compartida: cada cocina tiene sus propios ingredientes y utensilios
- Fallos independientes: si el restaurante de GDL pierde electricidad, CDMX y MTY continúan trabajando
- Paralelismo implícito: las tres cocinas trabajan simultáneamente

### 7.3 Diagrama - Distribuido (N=3 nodos, cada uno con P≥1 cores)

```
Arquitectura física:

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Nodo n₁   │◄───────►│   Nodo n₂   │◄───────►│   Nodo n₃   │
│   CDMX      │  δ₁₂    │     GDL     │  δ₂₃    │     MTY     │
│             │         │             │         │             │
│ CPU: τ₁     │         │ CPU: τ₂     │         │ CPU: τ₃     │
│ RAM local   │         │ RAM local   │         │ RAM local   │
└─────────────┘         └─────────────┘         └─────────────┘

Latencias de red: δ₁₂ = 50ms, δ₂₃ = 40ms, δ₁₃ = 60ms

Vista temporal (ejecución + comunicación):

n₁: [████████]─msg→
n₂:            [████████]─msg→
n₃:                       [████████]

Leyenda:
  █ = ejecución local en el nodo
  ─msg→ = envío de mensaje con latencia δ (comunicación por red)
```

### 7.4 Tabla de análisis temporal (conceptual)

| Fase | n₁ (CDMX) | n₂ (GDL) | n₃ (MTY) | Comunicación |
|------|-----------|----------|----------|--------------|
| I    | τ₁ EXEC   | —        | —        | —            |
| II   | Completa  | τ₂ EXEC  | —        | n₁→n₂ (δ₁₂)  |
| III  | Completa  | Completa | τ₃ EXEC  | n₂→n₃ (δ₂₃)  |

Notas:
- Cada nodo ejecuta su tarea localmente de forma independiente.
- La comunicación entre nodos introduce latencia δᵢⱼ.
- Si las tareas fueran independientes, podrían ejecutar en paralelo (Fase I simultánea en los 3 nodos).

### 7.5 Problema fundamental: relojes y tiempo en sistemas distribuidos

En sistemas con P cores en la misma máquina (sección 6), existe un **reloj global compartido**:
- Todos los cores ven el mismo tiempo físico (mismo cristal de cuarzo)
- Podemos decir con certeza "el evento A ocurrió antes que B" si comparamos sus timestamps
- La función T (tiempo) es única y compartida

En sistemas distribuidos, **NO existe reloj global**:

**Problema de los relojes distribuidos:**

Sea clockᵢ(t) el reloj local del nodo nᵢ en el instante "real" t.

En un sistema ideal: clockᵢ(t) = clock_j(t) = t para todo i, j.

En la realidad:
1. **Deriva de reloj (clock drift)**: cada reloj físico avanza a velocidad ligeramente diferente
   - clockᵢ(t) ≠ clock_j(t) incluso si se sincronizaron en t=0
   - Deriva típica: 10⁻⁶ (1 segundo por cada ~11 días)

2. **Desincronización inicial**: los relojes arrancan en momentos diferentes

3. **Imposibilidad de sincronización perfecta**: debido a latencia δᵢⱼ, no podemos sincronizar instantáneamente

**Consecuencias formales:**

Sea e₁ un evento en nodo n₁ con timestamp local t₁ = clock₁(e₁)  
Sea e₂ un evento en nodo n₂ con timestamp local t₂ = clock₂(e₂)

Si t₁ < t₂, **NO podemos concluir** que e₁ ocurrió antes que e₂ en tiempo real.

**Ejemplo concreto:**
```
Nodo n₁ (CDMX): clock₁ marca 10:00:00.000 cuando recibe pedido A
Nodo n₂ (GDL):  clock₂ marca 10:00:00.100 cuando recibe pedido B

¿Cuál pedido llegó primero en tiempo real? No lo sabemos con certeza.
Si clock₁ está adelantado 200ms, entonces B llegó antes que A.
```

**Soluciones en sistemas distribuidos:**

1. **Relojes lógicos de Lamport:**
   - No miden tiempo físico, sino orden causal de eventos
   - Cada nodo mantiene un contador L que incrementa con cada evento
   - Cuando nᵢ envía mensaje a nⱼ, incluye Lᵢ
   - nⱼ actualiza: Lⱼ = max(Lⱼ, Lᵢ) + 1
   - Garantía: si e₁ causó e₂, entonces L(e₁) < L(e₂)

2. **Vector clocks:**
   - Cada nodo mantiene un vector V de tamaños |N|
   - Vᵢ[i] = número de eventos en nodo nᵢ
   - Permite detectar concurrencia: si V₁ y V₂ no son comparables, los eventos son concurrentes

3. **Sincronización aproximada (NTP - Network Time Protocol):**
   - Intenta mantener relojes sincronizados con precisión de milisegundos
   - Usa múltiples servidores de tiempo y compensa latencia de red
   - Suficiente para muchas aplicaciones, pero no garantiza orden exacto

**Formalización del problema:**

En sistema paralelo (sección 6):
- Existe función global T: Events → ℝ⁺
- ∀ eventos e₁, e₂: T(e₁) < T(e₂) es decidible con certeza

En sistema distribuido (sección 7):
- Cada nodo tiene función local Tᵢ: Events_i → ℝ⁺
- NO existe función global T accesible a todos
- Relación "happened-before" (→) se define causalmente, no por tiempo físico:
  - e₁ → e₂ si: e₁ y e₂ están en el mismo nodo y e₁ ocurrió antes localmente, O
  - e₁ es envío de mensaje y e₂ es su recepción, O
  - existe e₃ tal que e₁ → e₃ y e₃ → e₂ (transitividad)

**Analogía de la cocina (relojes distribuidos):**

Cada restaurante (nodo) tiene su propio reloj de pared:
- Reloj de CDMX puede estar adelantado 2 minutos
- Reloj de GDL puede estar atrasado 1 minuto
- Reloj de MTY puede estar exacto

Cuando CDMX llama a GDL diciendo "son las 10:00, empiecen", GDL recibe el mensaje a las "9:59" según su reloj (pero ya pasaron segundos de latencia telefónica). No hay forma de saber el tiempo "real" absoluto; solo podemos establecer orden causal: "CDMX envió instrucción antes de que GDL la recibiera".

### 7.6 Propiedades clave de sistemas distribuidos

- **Escalabilidad horizontal**: agregar más nodos aumenta capacidad total
- **Tolerancia a fallos**: si un nodo falla, el sistema puede continuar (con degradación)
- **Latencia de red**: comunicación entre nodos es órdenes de magnitud más lenta que memoria local
- **CAP theorem**: en presencia de particiones de red, solo se pueden garantizar 2 de 3: Consistencia, Disponibilidad, Tolerancia a particiones
- **Sincronización distribuida**: relojes de nodos pueden estar desincronizados; se requieren algoritmos especiales (Lamport timestamps, vector clocks)
- **No hay tiempo global**: el orden de eventos se define causalmente, no por timestamps físicos

### 7.6 Diferencias con paralelismo (sección 6)

- Paralelismo (sección 6):
  - P ≥ 2 cores en la misma máquina
  - Memoria compartida (o muy rápida)
  - Latencia de comunicación: nanosegundos
  - Separación física: centímetros (dentro del mismo chip/placa)
  - Fallo de un core típicamente afecta toda la máquina

- Distribuido (sección 7):
  - N ≥ 2 nodos en máquinas separadas
  - Sin memoria compartida; comunicación por red
  - Latencia de comunicación: milisegundos a segundos
  - Separación física: metros a kilómetros
  - Fallo de un nodo es independiente de otros nodos

Relación: Distribuido implica paralelismo (múltiples CPUs trabajando), pero añade complejidad de red, fallos independientes y latencia significativa.

### 7.7 Composición: distribuido con paralelismo y concurrencia interna

Cada nodo en un sistema distribuido puede, a su vez:
- Tener P ≥ 1 cores locales (paralelismo dentro del nodo)
- Cada core puede manejar múltiples tareas (concurrencia/asincronía dentro del core)

**Ejemplo completo:**
- N=3 nodos distribuidos (CDMX, GDL, MTY)
- Cada nodo tiene P=4 cores locales
- Cada core maneja 10 tareas de forma asíncrona y concurrente

Esto da: 3 × 4 × 10 = 120 tareas totales en el sistema, con 3 niveles de paralelismo/concurrencia:
1. Distribuido: entre nodos (latencia alta)
2. Paralelo: entre cores dentro de un nodo (latencia baja)
3. Concurrente/asíncrono: entre tareas dentro de un core (sin paralelismo físico)

### 7.8 Implementación típica: procesos en nodos, hilos dentro de procesos

**Mecanismo de implementación:**

- **Nodos**: N ≥ 2 (máquinas físicamente separadas)
- **Procesos por nodo**: típicamente 1 proceso principal por nodo (puede tener múltiples)
- **Hilos por proceso**: cada proceso puede tener H ≥ 1 hilos
- **Cores por nodo**: cada nodo tiene P ≥ 1 cores locales
- **Comunicación**: paso de mensajes por red (sockets, MPI, RPC, HTTP, etc.)

**Características:**

1. Cada nodo ejecuta procesos independientes (memoria NO compartida entre nodos)
2. Comunicación entre nodos mediante red (latencia δᵢⱼ > 0)
3. Dentro de cada nodo: puede haber paralelismo local (P cores) y concurrencia (H hilos)
4. Fallos independientes: un nodo puede caer sin afectar a otros

**Formalización:**

Sea N = {n₁, n₂, ..., nₘ} el conjunto de nodos.

Sea Pᵢ el conjunto de procesos en nodo nᵢ.

Sea Hᵢⱼ el conjunto de hilos en proceso j del nodo i.

Sea location: Task → N la función que asigna tareas a nodos.

Comunicación entre τᵢ en nₐ y τⱼ en n_b (a ≠ b) requiere paso de mensaje con latencia δₐ_b.

**Ejemplos de tecnologías:**

1. **Frameworks de computación distribuida:**
   - Apache Spark (procesamiento de datos)
   - Hadoop MapReduce
   - Dask (Python distribuido)
   - Ray (ML distribuido)

2. **Paso de mensajes:**
   - MPI (Message Passing Interface) - HPC
   - gRPC - microservicios
   - ZeroMQ - messaging
   - RabbitMQ, Kafka - message brokers

3. **Orquestación:**
   - Kubernetes (containers en múltiples nodos)
   - Docker Swarm
   - Nomad

4. **Bases de datos distribuidas:**
   - Cassandra, MongoDB (sharding)
   - CockroachDB, TiDB

**Arquitectura típica de 3 niveles:**

```
Nivel 1 (Distribuido): N nodos comunicándose por red
  ↓
Nivel 2 (Paralelo): Cada nodo con P cores
  ↓
Nivel 3 (Concurrente/Asíncrono): Cada core con H tareas
```

**Ventajas:**
- Escalabilidad masiva (agregar más nodos)
- Tolerancia a fallos (redundancia)
- Procesamiento de datos que no caben en una máquina
- Geografía distribuida (latencia reducida para usuarios)

**Desventajas:**
- Complejidad máxima: red, fallos parciales, consistencia
- Latencia de comunicación (ms a segundos)
- Debugging muy difícil
- Problemas de sincronización distribuida (relojes, consensus)
- CAP theorem: trade-offs inevitables

**Cuándo usar:**
- Big Data (terabytes/petabytes)
- Alta disponibilidad crítica
- Carga que excede capacidad de una máquina
- Servicios globales (CDN, cloud)

---

## 8. MAPEO DE MODELOS A IMPLEMENTACIONES (VISTA PANORÁMICA)

Esta sección consolida la relación entre los modelos matemáticos (secciones 2-7) y sus mecanismos de implementación típicos.

### 8.1 Tabla Comparativa: Modelo × Mecanismo

| Modelo | H (hilos) | P (cores) | Mecanismo principal | Scheduler | Ejemplo tecnología |
|--------|-----------|-----------|---------------------|-----------|-------------------|
| **Secuencial** | 1 | 1 | Single thread bloqueante | No necesario | Script Python simple |
| **Asínc. no conc.** | 1 | 1 | Event loop ocioso | Event loop (sin aprovechar) | async/await sin gather |
| **Conc. no asínc.** | H > 1 | 1 | OS threads + time-slicing | Scheduler del OS | Python threading (GIL) |
| **Asínc. conc.** | 1 | 1 | Event loop + coroutines | Event loop activo | Node.js, asyncio |
| **Paralelo** | H ≥ P | P ≥ 2 | OS threads/processes | Scheduler del OS | multiprocessing, pthreads |
| **Distribuido** | Variable | Variable | Procesos en nodos + red | Distribuido | Spark, Kubernetes |

### 8.2 Ortogonalidad: Modelo Matemático vs Implementación

**Principio fundamental:** Las propiedades matemáticas (concurrencia, asincronía, paralelismo) son **independientes** del mecanismo de implementación.

**Ejemplos de ortogonalidad:**

1. **Concurrencia puede lograrse con:**
   - Múltiples OS threads en P=1 (sección 4)
   - Event loop con coroutines en P=1 (sección 5)
   - Green threads (Go, Erlang)
   - Procesos con IPC

2. **Asincronía puede lograrse con:**
   - Callbacks (JavaScript clásico)
   - Promises/Futures (JavaScript moderno)
   - async/await (Python, Rust, C#)
   - Channels (Go)
   - Actors (Erlang, Akka)

3. **Paralelismo puede lograrse con:**
   - OS threads (Java, C++)
   - OS processes (Python multiprocessing)
   - GPU threads (CUDA, OpenCL)
   - Distributed processes (MPI)

### 8.3 Decisión de Implementación: Árbol de Decisión

```
¿Múltiples máquinas físicas?
├─ Sí → DISTRIBUIDO (sección 7)
│        Implementación: procesos en nodos + red
│
└─ No → ¿Múltiples cores disponibles (P > 1)?
        ├─ Sí → ¿Tareas son CPU-bound?
        │       ├─ Sí → PARALELO (sección 6)
        │       │        Implementación: threads/processes en múltiples cores
        │       │
        │       └─ No (I/O-bound) → ASÍNC. CONC. + PARALELO
        │                Implementación: event loop + thread pool
        │
        └─ No (P=1) → ¿Tareas tienen waits (I/O)?
                ├─ Sí → ¿Quieres aprovechar los waits?
                │       ├─ Sí → ASÍNC. CONC. (sección 5)
                │       │        Implementación: event loop con coroutines
                │       │
                │       └─ No → ASÍNC. NO CONC. (sección 3)
                │                Implementación: event loop ocioso
                │
                └─ No (CPU-bound) → ¿Múltiples tareas?
                        ├─ Sí → CONC. NO ASÍNC. (sección 4)
                        │        Implementación: múltiples threads con time-slicing
                        │
                        └─ No → SECUENCIAL (sección 2)
                                 Implementación: single thread bloqueante
```

### 8.4 Casos Híbridos Comunes en la Práctica

**1. Servidor web moderno:**
- Distribuido: múltiples nodos (load balancer)
- Paralelo: cada nodo con P cores
- Asínc. conc.: event loop en cada core
- Ejemplo: Node.js cluster + PM2 en Kubernetes

**2. Aplicación de machine learning:**
- Distribuido: cluster de GPUs (Ray, Horovod)
- Paralelo: múltiples GPUs por nodo
- Paralelo interno: miles de threads en GPU
- Ejemplo: PyTorch Distributed

**3. Base de datos distribuida:**
- Distribuido: sharding en N nodos
- Paralelo: queries paralelas en cada nodo
- Asínc. conc.: conexiones concurrentes por nodo
- Ejemplo: Cassandra, CockroachDB

**4. Sistema operativo:**
- Paralelo: procesos en múltiples cores
- Conc. no asínc.: time-slicing de procesos
- Asínc. conc.: I/O asíncrono (epoll, kqueue)
- Ejemplo: Linux kernel

### 8.5 Resumen: Abstracción → Implementación

**Capa 1 (Abstracción matemática):**
- Tareas τᵢ con exec(τᵢ), wait(τᵢ)
- Propiedades: concurrencia, asincronía, paralelismo
- Independiente de implementación

**Capa 2 (Mecanismos de implementación):**
- Threads, processes, coroutines, actors
- Función impl: Task → Mecanismo
- Múltiples opciones para cada modelo

**Capa 3 (Hardware):**
- Cores (P), nodos (N), red (δᵢⱼ)
- Restricciones físicas reales
- Determina límites de rendimiento

**Relación:**
```
Modelo matemático (secciones 2-7)
    ↓ (puede implementarse con)
Mecanismo (threads, processes, coroutines, etc.)
    ↓ (ejecuta en)
Hardware (cores, nodos, red)
```

La elección del mecanismo depende de:
1. Propiedades del modelo deseadas
2. Hardware disponible
3. Lenguaje/framework utilizado
4. Trade-offs (complejidad vs rendimiento)

---

