# Framework Matemático Formal: Modelos de Ejecución Computacional

## Glosario de Términos Fundamentales

### ¿Qué es "esperar" (wait)?

**Definición intuitiva:** Cuando una tarea está "esperando", significa que **ya inició su trabajo pero no puede continuar** hasta que ocurra algo externo. Durante este tiempo de espera, **NO se está realizando cómputo** (procesamiento activo por la CPU).

**Ejemplos concretos de espera:**

1. **Esperar I/O (Input/Output - Entrada/Salida):**
   - Leer un archivo del disco duro: la CPU pide datos, pero el disco mecánico tarda milisegundos en encontrarlos y leerlos
   - Descargar datos de internet: esperamos que los datos viajen por la red
   - Esperar input del usuario: el programa espera que el usuario teclee algo

2. **Esperar otros recursos:**
   - Esperar que una base de datos responda a una consulta
   - Esperar que un mutex/lock se libere (en programación concurrente)
   - Esperar que un temporizador termine

**Clave:** Durante la espera, **otro proceso podría usar la CPU**. No estamos "pensando" (computando), solo aguardando que algo externo complete.

### Hilos (Threads) y Procesos

**Proceso:** Programa en ejecución con su propio espacio de memoria independiente. Como tener aplicaciones separadas abiertas (Chrome, Word, Spotify).

**Hilo (Thread):** Unidad de ejecución dentro de un proceso que comparte memoria con otros hilos del mismo proceso. Como tener múltiples pestañas en Chrome que comparten recursos.

**Analogía:** 
- **Proceso** = Casa completa con su cocina, comedor, recursos propios
- **Hilo** = Personas dentro de la misma casa compartiendo la cocina

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
- Ejemplo: start(τ₁) = 0 significa "la tarea 1 inicia en t=0 segundos"

**end(τᵢ) ∈ T:** Instante de tiempo cuando τᵢ termina completamente
- Ejemplo: end(τ₁) = 10 significa "la tarea 1 termina en t=10 segundos"

**exec(τᵢ) ⊆ T:** Conjunto de todos los instantes donde la CPU está ejecutando activamente τᵢ
- Ejemplo: exec(τ₁) = [0, 2] ∪ [5, 7] significa "la CPU trabajó en τ₁ de 0 a 2 segundos, luego de 5 a 7 segundos"
- **Interpretación:** Momentos donde hay **cómputo activo** (la CPU procesa instrucciones)

**wait(τᵢ) ⊆ T:** Conjunto de todos los instantes donde τᵢ está esperando (sin cómputo)
- Ejemplo: wait(τ₁) = [2, 5] significa "τ₁ esperó de 2 a 5 segundos (quizás esperando datos de disco)"
- **Interpretación:** Momentos donde **NO hay cómputo** (esperando algo externo)

### 1.4 Restricciones Fundamentales

Para cada tarea τᵢ:

1. **exec(τᵢ) ∩ wait(τᵢ) = ∅**
   - No puedes ejecutar y esperar simultáneamente
   - Es como no puedes estar corriendo y sentado al mismo tiempo

2. **exec(τᵢ) ∪ wait(τᵢ) = [start(τᵢ), end(τᵢ)]**
   - Entre inicio y fin, o estás ejecutando o esperando (no hay otro estado)
   - Todo el tiempo de vida de la tarea se divide en estos dos estados

### 1.5 Notación para Instantes Específicos

Sea **t** un instante específico de tiempo (un punto en T).

Definimos el conjunto de tareas ejecutándose en t:

**ExecutingAt(t)** = {τᵢ ∈ Task | t ∈ exec(τᵢ)}

**Interpretación:** "¿Qué tareas están usando la CPU en el instante t?"

**Cardinalidad:** |ExecutingAt(t)| nos dice cuántas tareas se ejecutan simultáneamente en t.

---

## 2. SECUENCIAL

### 2.1 Definición Matemática Formal

Un sistema es **secuencial** si y solo si:

**∀ τᵢ, τⱼ ∈ Task, i ≠ j:** (end(τᵢ) ≤ start(τⱼ)) **OR** (end(τⱼ) ≤ start(τᵢ))

**Interpretación:** Para cualquier par de tareas diferentes, una debe terminar completamente antes de que la otra comience.

**Propiedades derivadas:**

1. **|ExecutingAt(t)| = 1** para todo t donde existe ejecución
   - Exactamente una tarea ejecutándose en cualquier momento

2. Las tareas forman una secuencia totalmente ordenada
   - Hay un orden estricto: τ₁ → τ₂ → τ₃ → ...

3. No hay solapamiento temporal entre intervalos [start(τᵢ), end(τᵢ)]

### 2.2 Diagrama de Gantt - Secuencial

```
Tarea    0    2    4    6    8    10   12   14   16   18   20
τ₁ (moler) [████████]
τ₂ (hervir)          [████████████]
τ₃ (café)                         [████████████████]
τ₄ (tostar)                                       [██████]
τ₅ (huevos)                                             [████████████]

Leyenda: █ = ejecución activa
```

### 2.3 Código Python - Secuencial

```python
import time

def moler_cafe():
    print("t=0: Iniciando moler café...")
    time.sleep(3)  # Simula 3 segundos de trabajo
    print("t=3: Café molido completado")

def hervir_agua():
    print("t=3: Iniciando hervir agua...")
    time.sleep(4)
    print("t=7: Agua hervida")

def preparar_cafe():
    print("t=7: Iniciando preparar café...")
    time.sleep(6)
    print("t=13: Café listo")

# EJECUCIÓN SECUENCIAL
inicio = time.time()
moler_cafe()      # Bloquea hasta terminar
hervir_agua()     # Inicia solo cuando moler_cafe() terminó
preparar_cafe()   # Inicia solo cuando hervir_agua() terminó
print(f"Tiempo total: {time.time() - inicio:.1f} segundos")
```

**Keywords Python:**
- `time.sleep(n)`: Pausa la ejecución n segundos (simula trabajo)
- Las funciones se llaman una tras otra, cada una bloquea hasta completar

### 2.4 Analogía del Mundo Real

**Escenario:** Persona haciendo TODO el desayuno paso por paso, esperando que cada cosa termine antes de iniciar la siguiente.

**Ejecución:**
1. [0-3 min]: Muelo café. Me quedo observando el molinillo. **No inicio nada más.**
2. [3-7 min]: Hiervo agua en tetera. Me quedo frente a la tetera. **Todo lo demás espera.**
3. [7-13 min]: Preparo café en cafetera. Observo el goteo. **No toco nada más.**
4. [13-15 min]: Tosto pan. Observo la tostadora.
5. [15-20 min]: Preparo huevos revueltos en sartén.

**Tiempo total:** 20 minutos

**Propiedad clave:** En el instante t=5, solo hay una actividad: hervir agua. En t=14, solo tostar pan.

---

## 3. ASÍNCRONO NO CONCURRENTE

### 3.1 Definición Matemática Formal

Un sistema es **asíncrono no concurrente** si:

1. **∀ τᵢ, τⱼ ∈ Task, i ≠ j:** exec(τᵢ) ∩ exec(τⱼ) = ∅
   - **Interpretación:** Nunca dos tareas ejecutan simultáneamente en la CPU

2. **∃ τᵢ, τⱼ ∈ Task:** wait(τᵢ) ∩ [start(τⱼ), end(τⱼ)] ≠ ∅
   - **Interpretación:** Existe al menos una tarea que está esperando mientras otra está activa

3. **Número de procesadores:** P = 1
   - Solo una CPU disponible

**Propiedades derivadas:**

1. **|ExecutingAt(t)| ≤ 1** para todo t
   - Máximo una tarea ejecutándose activamente

2. Durante wait(τᵢ), el procesador puede iniciar/continuar otras tareas

### 3.2 Diagrama de Gantt - Asíncrono No Concurrente (CORREGIDO)

**Diagrama Multi-Vista: Separación explícita entre CPU y estados de tareas**
```
Escala de tiempo:  0.0   1.0   2.0   3.0   4.0   5.0   6.0   6.5 7.0
                   |     |     |     |     |     |     |     |   |
τ₁ (cafetera)      [█]░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░[█]
                   ↑                                           ↑
                   0.5s                                        6.6s

τ₂ (tostadora)     [█]░░░░░░░░░░░░░░░░░░░░░░░░░░░[█]
                   ↑                             ↑ ↑
                   0.5s 0.7s                   2.7s 2.8s

τ₃ (leer)              [████████████████████]░[████████████████]
                       ↑                    ↑ ↑                ↑
                       0.7s               2.7s 2.8s            6.5s

Leyenda:
  █ = ejecución activa (usando CPU)
  ░ = esperando/interrumpido (CPU ocupada por otra tarea)
  ↑ = marca de tiempo exacta

Análisis por instantes:
  t=0.0-0.5: CPU ejecuta τ₁ (configurar cafetera)          [0.5s CPU]
  t=0.5-0.7: CPU ejecuta τ₂ (poner pan en tostadora)      [0.2s CPU]
  t=0.7-2.7: CPU ejecuta τ₃ (leer periódico - parte 1)    [2.0s CPU]
  t=2.7-2.8: CPU ejecuta τ₂ (sacar pan)                   [0.1s CPU] ← τ₃ INTERRUMPIDO
  t=2.8-6.5: CPU ejecuta τ₃ (leer periódico - parte 2)    [3.7s CPU]
  t=6.5-6.6: CPU ejecuta τ₁ (servir café)                 [0.1s CPU]

CORRECCIÓN: τ₃ se interrumpe brevemente en t=2.7-2.8 cuando τ₂ necesita la CPU
```

**TABLA DE ANÁLISIS TEMPORAL:**

| Intervalo | CPU ejecuta | τ₁ estado | τ₂ estado | τ₃ estado | Dispositivos activos |
|-----------|-------------|-----------|-----------|-----------|---------------------|
| 0.0-0.5 | **τ₁** | EXEC | No iniciada | No iniciada | Ninguno |
| 0.5-0.7 | **τ₂** | WAIT | EXEC | No iniciada | Cafetera |
| 0.7-2.7 | **τ₃** | WAIT | WAIT | EXEC | Cafetera, Tostadora |
| 2.7-2.8 | **τ₂** | WAIT | EXEC | Pausada | Cafetera |
| 2.8-6.5 | **τ₃** | WAIT | Completa | EXEC | Cafetera |
| 6.5-6.6 | **τ₁** | EXEC | Completa | Pausada | Ninguno |
| 6.6-7.0 | **τ₃** | Completa | Completa | EXEC | Ninguno |

**PROPIEDADES CLAVE:**

1. **P = 1 (un solo procesador):** La CPU solo ejecuta UNA tarea en cada instante
2. **Aprovechamiento de wait:** Mientras cafetera/tostadora trabajan solas, CPU hace otras cosas
3. **No hay paralelismo:** exec(τ₁) ∩ exec(τ₂) = ∅, exec(τ₁) ∩ exec(τ₃) = ∅, exec(τ₂) ∩ exec(τ₃) = ∅
4. **Hay concurrencia temporal:** Las tres tareas tienen sus intervalos [start, end] solapados
5. **Tiempo total:** 7.0 segundos (vs ~9+ segundos secuencial)

### 3.3 Código Python - Asíncrono No Concurrente

```python
import asyncio  # Librería para programación asíncrona

# Simulamos tareas con períodos de espera
async def preparar_cafetera():
    print("t=0.0: [CPU ACTIVA] Configurando cafetera...")
    await asyncio.sleep(0.5)  # Trabajo activo
    
    print("t=0.5: [ESPERANDO] Cafetera goteando (CPU libre)...")
    await asyncio.sleep(6)  # Wait state - CPU puede hacer otras cosas
    
    print("t=6.5: [CPU ACTIVA] Sirviendo café...")
    await asyncio.sleep(0.1)

async def tostar_pan():
    print("t=0.5: [CPU ACTIVA] Poniendo pan en tostadora...")
    await asyncio.sleep(0.2)
    
    print("t=0.7: [ESPERANDO] Pan tostándose (CPU libre)...")
    await asyncio.sleep(2)
    
    print("t=2.7: [CPU ACTIVA] Sacando pan...")
    await asyncio.sleep(0.1)

async def leer_periodico():
    print("t=0.7: [CPU ACTIVA] Leyendo periódico...")
    await asyncio.sleep(5.8)  # Trabajo continuo

# EJECUCIÓN ASÍNCRONA NO CONCURRENTE
async def main():
    inicio = asyncio.get_event_loop().time()
    
    # asyncio.gather ejecuta tareas concurrentemente (pero no en paralelo)
    # Alterna entre ellas cuando hay wait states
    await asyncio.gather(
        preparar_cafetera(),
        tostar_pan(),
        leer_periodico()
    )
    
    print(f"Tiempo total: {asyncio.get_event_loop().time() - inicio:.1f}s")

asyncio.run(main())
```

**Keywords Python:**
- `async def`: Define función asíncrona
- `await`: Marca punto donde la función puede pausarse (wait state)
- `asyncio.gather()`: Ejecuta múltiples funciones asíncronas, alternando entre ellas
- `asyncio.sleep()`: Simula espera (libera CPU para otras tareas)

### 3.4 Analogía del Mundo Real

**Escenario:** Una persona sola delegando trabajo a electrodomésticos autónomos.

**Ejecución:**
1. [0:00-0:30]: **[TRABAJO ACTIVO]** Configuro cafetera con agua y café
2. [0:30-6:30]: **[ESPERA]** Cafetera gotea sola → Durante este tiempo:
   - [0:30-0:45]: **[TRABAJO ACTIVO]** Pongo pan en tostadora
   - [0:45-2:45]: **[ESPERA]** Tostadora trabaja sola → Durante este tiempo:
     - [0:45-6:30]: **[TRABAJO ACTIVO]** Leo el periódico
   - [2:45-2:50]: **[TRABAJO ACTIVO]** Saco pan
3. [6:30-6:35]: **[TRABAJO ACTIVO]** Sirvo café

**Propiedad clave:** Solo una acción física a la vez (P=1), pero aprovecho los wait states.

---

## 4. CONCURRENTE

### 4.1 Definición Matemática Formal

Un sistema es **concurrente** si:

**∃ τᵢ, τⱼ ∈ Task, i ≠ j:** [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅

**Interpretación:** Existen al menos dos tareas cuyos intervalos de vida se solapan temporalmente.

**Características:**
- Concurrencia es una **propiedad estructural** del problema, no de la ejecución física
- No especifica si exec(τᵢ) ∩ exec(τⱼ) = ∅ o no
- No especifica P (número de procesadores)
- Indica que múltiples tareas están "en progreso" simultáneamente

**Nota importante:** Concurrente ≠ Paralelo. Concurrencia es sobre la estructura (múltiples tareas iniciadas pero no terminadas), paralelismo es sobre ejecución física simultánea.

### 4.2 Diagrama Conceptual - Concurrencia

```
Vista temporal (estructura del problema):

Mesa 1: |════════════τ₁════════════|
           Mesa 2: |═════τ₂═════|
              Mesa 3: |══════════τ₃══════════|
         t=0    t=2 t=3          t=8        t=12

Interpretación: Las tres órdenes tienen sus períodos [start, end] solapados.
Esto ES concurrencia (estructura), independiente de cómo se ejecuten físicamente.
```

### 4.3 Analogía del Mundo Real

**Escenario:** Sistema de pedidos en un restaurante.

**Tareas (pedidos de clientes):**
- τ₁: Mesa 1 pide café y tostadas [llega t=0, se completa t=8]
- τ₂: Mesa 2 pide jugo [llega t=2, se completa t=6]
- τ₃: Mesa 3 pide omelette [llega t=3, se completa t=12]

**Concurrencia:** En t=4, las tres órdenes están "activas" (iniciadas pero no completadas). Esto es concurrencia estructural.

**Cómo se ejecutan** estas tareas concurrentes puede variar:
- Un mesero alternando entre mesas (concurrente no paralelo)
- Tres meseros, uno por mesa (paralelo)

---

## 5. CONCURRENTE NO ASÍNCRONO

### 5.1 Definición Matemática Formal

Un sistema es **concurrente no asíncrono** si:

1. **∃ τᵢ, τⱼ ∈ Task:** [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅
   - **Interpretación:** Hay concurrencia (solapamiento temporal)

2. **∀ τᵢ ∈ Task:** wait(τᵢ) = ∅
   - **Interpretación:** Ninguna tarea tiene períodos de espera (todas son CPU-bound)

3. **∀ τᵢ, τⱼ ∈ Task, i ≠ j:** exec(τᵢ) ∩ exec(τⱼ) = ∅
   - **Interpretación:** No hay ejecución simultánea física

4. **P = 1** (un solo procesador)

**Mecanismo:** Time-slicing (división del tiempo) con quantum q.

Sea **quantum q > 0:** intervalo de tiempo que la CPU dedica a una tarea antes de cambiar.

**Propiedades:**
- **|ExecutingAt(t)| = 1** para todo t con ejecución
- Alternancia rápida entre tareas (context switching)
- Todas las tareas requieren CPU continuamente (CPU-bound)

### 5.2 Diagrama de Gantt - Concurrente No Asíncrono (MEJORADO)

```
Context Switching con quantum q=20s

Tiempo:  0    20   40   60   80   100  120  140  160
τ₁ (risotto)  [██████]     [██████]     [██████]     
τ₂ (salsa)           [██████]     [██████]     [██████]
τ₃ (vegetales)              [██████]     [██████]     [██████]

Leyenda: █ = ejecución activa (20s cada turno)

ACLARACIÓN CRÍTICA SOBRE LAS TAREAS:
════════════════════════════════════════════════════════════════

τ₁, τ₂, τ₃ son tareas CONTINUAS que NO terminan hasta el final.
Cada bloque █ representa un "quantum" de ejecución de la MISMA tarea.

**¿Por qué no hay "wait"?**
Porque estas tareas son CPU-bound (intensivas en CPU). Requieren
atención constante:
- Risotto: requiere revolver CONSTANTEMENTE
- Salsa: requiere batir CONSTANTEMENTE  
- Vegetales: requieren mover sartén CONSTANTEMENTE

**¿Qué pasa entre los bloques █ de una misma tarea?**
La tarea está PAUSADA (no ejecutando), pero NO está en "wait".
WAIT implica esperar algo externo (I/O, red, timer).
Aquí simplemente la CPU cambió a otra tarea (context switch).

**Estado de cada tarea en cada momento:**
t=10:  τ₁ ejecutando, τ₂ lista (esperando turno), τ₃ lista
t=30:  τ₂ ejecutando, τ₁ lista, τ₃ lista
t=50:  τ₃ ejecutando, τ₁ lista, τ₂ lista

**Las tareas NO se completan individualmente** - todas avanzan
simultáneamente mediante time-slicing hasta que las tres terminan.

**Diferencia con wait:**
- WAIT = "esperando algo externo" → CPU libre para otros
- PAUSED = "esperando mi turno de CPU" → todavía necesito CPU
```

**Análisis temporal detallado:**

```
Estado de las tareas:

[0-20s]:   τ₁ EJECUTANDO | τ₂ LISTA (espera turno) | τ₃ LISTA
[20-40s]:  τ₁ LISTA      | τ₂ EJECUTANDO           | τ₃ LISTA  
[40-60s]:  τ₁ LISTA      | τ₂ LISTA                | τ₃ EJECUTANDO
[60-80s]:  τ₁ EJECUTANDO | τ₂ LISTA                | τ₃ LISTA
... continúa hasta que todas completan su trabajo total
```

### 5.3 Código Python - Concurrente No Asíncrono

```python
import threading
import time

# Variable global para simular CPU única
cpu_lock = threading.Lock()  # Solo un hilo puede tener el lock
quantum = 0.02  # 20ms quantum (simulado)

def tarea_intensiva_cpu(nombre, duracion_total):
    tiempo_trabajado = 0
    
    while tiempo_trabajado < duracion_total:
        # Adquirir CPU (solo uno a la vez)
        cpu_lock.acquire()
        
        print(f"t={time.time():.2f}: [CPU] {nombre} ejecutando...")
        time.sleep(quantum)  # Trabaja por un quantum
        
        cpu_lock.release()  # Liberar CPU para otros
        
        tiempo_trabajado += quantum
        time.sleep(0.001)  # Pequeña pausa para context switch

# Crear 3 hilos (threads) que compiten por 1 CPU
hilo1 = threading.Thread(target=tarea_intensiva_cpu, args=("Risotto", 0.1))
hilo2 = threading.Thread(target=tarea_intensiva_cpu, args=("Salsa", 0.1))
hilo3 = threading.Thread(target=tarea_intensiva_cpu, args=("Vegetales", 0.1))

inicio = time.time()
hilo1.start()
hilo2.start()
hilo3.start()

hilo1.join()  # Esperar a que termine
hilo2.join()
hilo3.join()

print(f"Tiempo total: {time.time() - inicio:.2f}s")
```

**Keywords Python:**
- `threading.Thread`: Crea un hilo (unidad de ejecución)
- `threading.Lock()`: Cerrojo que solo un hilo puede tener (simula CPU única)
- `.acquire()`: Tomar el lock (obtener CPU)
- `.release()`: Liberar el lock (liberar CPU)
- `.start()`: Iniciar hilo
- `.join()`: Esperar que hilo termine

### 5.4 Analogía del Mundo Real

**Escenario:** Chef preparando tres platos que requieren atención constante (CPU-bound).

**Tareas intensivas:**
- τ₁: Risotto (requiere revolver constantemente)
- τ₂: Salsa holandesa (requiere batir constantemente)
- τ₃: Vegetales salteados (requiere mover sartén constantemente)

**Ejecución con quantum q=20s:**

```
[0-20s]:    Revuelvo risotto
[20-40s]:   Bato salsa (risotto NO se mueve - se enfría un poco)
[40-60s]:   Salteo vegetales (otros quietos)
[60-80s]:   Revuelvo risotto nuevamente
...continúa rotando hasta que los tres platos estén listos...
```

**Propiedad clave:** 
- Solo una actividad física a la vez (P=1)
- Las tres tareas "avanzan simultáneamente" por alternancia
- NO hay wait states naturales (todas son CPU-bound)
- Cada tarea es una sola tarea continua que se ejecuta en fragmentos

**Diferencia crucial con secuencial:** En secuencial, el risotto se completaría totalmente antes de iniciar la salsa. Aquí, las tres tareas progresan "simultáneamente" mediante alternancia.

---

## 6. ASÍNCRONO Y CONCURRENTE

### 6.1 Definición Matemática Formal

Un sistema es **asíncrono y concurrente** si:

1. **∃ τᵢ, τⱼ ∈ Task:** [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅
   - Hay concurrencia

2. **∃ τₖ ∈ Task:** wait(τₖ) ≠ ∅
   - Hay asincronía

3. **∀ τᵢ, τⱼ ∈ Task, i ≠ j:** exec(τᵢ) ∩ exec(τⱼ) = ∅
   - No ejecución simultánea

4. **P = 1**

**Mecanismo:** El procesador único aprovecha wait states de unas tareas para ejecutar otras.

### 6.2 Diagrama de Gantt - Asíncrono y Concurrente (CORREGIDO)

```
Tiempo:   0    1    2    3    4    5    6    7    8    9    10
τ₁ (café)     [█]░░░░░░░░░░░░░░░░░░░░░░[█]
τ₂ (huevos)      [██]░░░░░░░░░░░░░░░░░░░░░░░░░[█]
τ₃ (pan)            [█]░░░░[█]
τ₄ (fruta)             [████████████]

Leyenda:
█ = CPU ejecutando activamente
░ = Esperando (dispositivo trabajando, CPU libre)

Análisis detallado por intervalos:
════════════════════════════════════════════════════════════════
t=0.0-0.5:   CPU ejecuta τ₁ (configurar cafetera)
t=0.5-6.5:   τ₁ en WAIT (cafetera gotea sola)

t=0.5-1.5:   CPU ejecuta τ₂ (preparar huevos, meter al horno)
t=1.5-9.5:   τ₂ en WAIT (huevos en horno)

t=1.5-1.75:  CPU ejecuta τ₃ (poner pan en tostadora)
t=1.75-3.75: τ₃ en WAIT (pan tostándose)

t=1.75-5.75: CPU ejecuta τ₄ (cortar fruta - trabajo continuo)
             ← AQUÍ la CPU trabaja CONTINUAMENTE sin wait

t=3.75-3.80: CPU ejecuta τ₃ (sacar pan de tostadora)
             τ₃ COMPLETA

t=3.80-5.75: CPU continúa con τ₄ (terminar de cortar fruta)
             τ₄ COMPLETA

t=5.75-6.5:  CPU IDLE (esperando que café y huevos terminen)

t=6.5-6.55:  CPU ejecuta τ₁ (servir café)
             τ₁ COMPLETA

t=6.55-9.5:  CPU IDLE (esperando huevos)

t=9.5-9.55:  CPU ejecuta τ₂ (sacar huevos del horno)
             τ₂ COMPLETA
```

### 6.3 Código Python - Asíncrono y Concurrente

```python
import asyncio

async def preparar_cafe():
    print("t=0.0: [CPU] Configurando cafetera...")
    await asyncio.sleep(0.5)  # Trabajo activo
    
    print("t=0.5: [WAIT] Cafetera goteando...")
    await asyncio.sleep(5)  # Wait - CPU disponible
    
    print("t=5.5: [CPU] Sirviendo café")
    return "Café listo"

async def preparar_huevos():
    print("t=0.5: [CPU] Preparando mezcla de huevos...")
    await asyncio.sleep(1)
    
    print("t=1.5: [WAIT] Huevos en horno...")
    await asyncio.sleep(8)
    
    print("t=9.5: [CPU] Sacando huevos")
    return "Huevos listos"

async def tostar_pan():
    print("t=1.5: [CPU] Poniendo pan...")
    await asyncio.sleep(0.25)
    
    print("t=1.75: [WAIT] Pan tostando...")
    await asyncio.sleep(2)
    
    print("t=3.75: [CPU] Sacando pan")
    return "Pan listo"

async def cortar_fruta():
    print("t=1.75: [CPU] Cortando fruta...")
    await asyncio.sleep(4)  # Trabajo continuo
    print("t=5.75: Fruta lista")
    return "Fruta lista"

async def main():
    inicio = asyncio.get_event_loop().time()
    
    # Ejecutar todas concurrentemente, aprovechando wait states
    resultados = await asyncio.gather(
        preparar_cafe(),
        preparar_huevos(),
        tostar_pan(),
        cortar_fruta()
    )
    
    print(f"\nTodo listo: {resultados}")
    print(f"Tiempo total: {asyncio.get_event_loop().time() - inicio:.1f}s")

asyncio.run(main())
```

### 6.4 Analogía del Mundo Real

**Escenario:** Chef preparando desayuno complejo aprovechando tiempos de espera.

**Ejecución optimizada:**
1. [0:00-0:30]: **[CPU]** Configuro cafetera
2. [0:30-1:30]: **[CPU]** Preparo huevos (mientras café **ESPERA**)
3. [1:30-1:45]: **[CPU]** Pongo pan (mientras café y huevos **ESPERAN**)
4. [1:45-3:45]: **[CPU]** Corto fruta (mientras todo **ESPERA**)
5. [3:45-5:30]: **[CPU]** Continúo fruta
6. [5:30-5:35]: **[CPU]** Sirvo café
7. [9:30-9:40]: **[CPU]** Saco huevos del horno

**Tiempo total:** ~10 minutos (vs 20+ minutos secuencial)

---

## 7. PARALELO

### 7.1 Definición Matemática Formal

Un sistema es **paralelo** si:

**∃ τᵢ, τⱼ ∈ Task, i ≠ j, ∃ t ∈ T:** (t ∈ exec(τᵢ)) **AND** (t ∈ exec(τⱼ))

**Interpretación:** Existe al menos un instante t donde dos tareas diferentes se ejecutan simultáneamente.

**Requisitos:**
- **P ≥ 2** (mínimo dos procesadores físicos)
- **|ExecutingAt(t)| ≥ 2** para algún t

**Relación con concurrencia:**
- Paralelo ⊆ Concurrente (todo sistema paralelo es concurrente)
- Concurrente ⊄ Paralelo (no toda concurrencia es paralela)

**CRÍTICO - Aclaración sobre hilos:**

**"Múltiples hilos" NO implica paralelismo automáticamente.**

Sea:
- H = número de hilos
- P = número de procesadores físicos

**Si H > P:** Necesariamente algunos hilos NO son paralelos (se ejecutan por time-slicing).

**Ejemplo:**
- 10 hilos en una máquina con P=1 (un núcleo) → Concurrente NO paralelo
- 10 hilos en una máquina con P=4 (cuatro núcleos) → Máximo 4 paralelos simultáneamente

### 7.2 Diagrama de Gantt - Paralelo

```
Procesadores físicos (P=2):

Tiempo:     0         5         10        15
CPU_A:   [████████████████ τ₁ ████████████████]
CPU_B:   [████████████████ τ₂ ████████████████]

Interpretación: En t=7, AMBAS CPUs ejecutan simultáneamente.
exec(τ₁) ∩ exec(τ₂) = [0,15] ≠ ∅
```

### 7.3 Código Python - Paralelo

```python
import multiprocessing  # Para paralelismo real
import time
import os

def tarea_intensiva(nombre, duracion):
    """Tarea que requiere CPU constante"""
    pid = os.getpid()  # ID del proceso (cada uno en CPU diferente)
    print(f"{nombre} iniciando en proceso {pid}")
    
    inicio = time.time()
    # Simular trabajo intensivo de CPU
    while time.time() - inicio < duracion:
        _ = sum(range(100000))  # Cálculo que usa CPU
    
    print(f"{nombre} completado en proceso {pid}")
    return f"{nombre} terminado"

if __name__ == "__main__":
    inicio = time.time()
    
    # Crear 2 procesos (Python ejecuta en CPUs separadas)
    proceso1 = multiprocessing.Process(
        target=tarea_intensiva, 
        args=("Risotto", 3)
    )
    proceso2 = multiprocessing.Process(
        target=tarea_intensiva, 
        args=("Salsa", 3)
    )
    
    # Iniciar ambos procesos (ejecutan en paralelo real)
    proceso1.start()
    proceso2.start()
    
    # Esperar que ambos terminen
    proceso1.join()
    proceso2.join()
    
    print(f"Tiempo total: {time.time() - inicio:.1f}s")
    print("Con 2 CPUs: ~3s. Si fuera secuencial: ~6s")
```

**Keywords Python:**
- `multiprocessing.Process`: Crea proceso separado (puede ejecutar en CPU diferente)
- `os.getpid()`: Obtiene ID del proceso (confirma que son procesos distintos)
- `.start()`: Inicia proceso (OS lo asigna a CPU disponible)
- `.join()`: Espera que proceso termine

### 7.4 Analogía del Mundo Real

**Escenario:** Dos chefs trabajando simultáneamente en la misma cocina.

**Hardware:** P = 2 chefs (dos procesadores físicos independientes)

**Tareas:**
- τ₁: Chef A prepara risotto [15 min de trabajo continuo]
- τ₂: Chef B prepara salsa [15 min de trabajo continuo]

**Ejecución paralela:**

```
[0:00-15:00] → Chef A revuelve risotto (CPU_A trabajando)
             → Chef B bate salsa (CPU_B trabajando)
             SIMULTÁNEAMENTE
```

**En t=7:30:**
- Chef A está revolviendo (exec(τ₁))
- Chef B está batiendo (exec(τ₂))
- Hay ejecución física simultánea: exec(τ₁) ∩ exec(τ₂) ≠ ∅

**Tiempo total:** 15 minutos (vs 30 minutos secuencial)

---

## 8. DISTRIBUIDO

### 8.1 Definición Matemática Formal

Sea **N** = {n₁, n₂, ..., nₘ} un conjunto de nodos computacionales.

Sea **location: Task → N** una función que asigna cada tarea a un nodo.

Sea **distance: N × N → ℝ⁺** una función de distancia física entre nodos.

Un sistema es **distribuido** si:

1. **|N| ≥ 2** (múltiples nodos)

2. **∀ nᵢ, nⱼ ∈ N, i ≠ j: ∃ δᵢⱼ > 0**
   - **Interpretación:** Existe latencia de red entre nodos (tiempo de comunicación)

3. **∃ τᵢ, τⱼ ∈ Task:** location(τᵢ) ≠ location(τⱼ)
   - **Interpretación:** Tareas ejecutan en nodos diferentes

4. **∀ nᵢ, nⱼ ∈ N, i ≠ j:** distance(nᵢ, nⱼ) ≥ d_min
   - **Interpretación:** Separación física significativa (típicamente > 1 metro)

**Propiedades adicionales:**
- No hay memoria compartida global entre todos los nodos
- Posibilidad de fallos parciales independientes
- Comunicación mediante paso de mensajes con latencia
- Distribuido ⊂ Paralelo ⊂ Concurrente

### 8.2 Diagrama - Sistema Distribuido

```
Arquitectura física:

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Nodo N₁   │◄───────►│   Nodo N₂   │◄───────►│   Nodo N₃   │
│   CDMX      │  δ₁₂    │ Guadalajara │  δ₂₃    │  Monterrey  │
│             │         │             │         │             │
│ CPU: τ₁     │         │ CPU: τ₂     │         │ CPU: τ₃     │
│ RAM local   │         │ RAM local   │         │ RAM local   │
└─────────────┘         └─────────────┘         └─────────────┘

Latencias: δ₁₂ = 50ms, δ₂₃ = 40ms, δ₁₃ = 60ms


Diagrama de Gantt temporal:

Tiempo:    0    1    2    3    4    5    6
N₁ (τ₁): [████████]─┐
                     └─msg→
N₂ (τ₂):            [████████]─┐
                               └─msg→
N₃ (τ₃):                      [████████]

Leyenda: 
█ = ejecución local
─msg→ = envío de mensaje con latencia δ
```

### 8.3 Código Python - Distribuido (Conceptual)

```python
# NOTA: Este código es conceptual (requiere configuración de red real)
# Muestra la estructura de un sistema distribuido

from multiprocessing import Process
import socket
import time

def nodo_cdmx(puerto=5000):
    """Nodo 1: Prepara platos principales"""
    print("[CDMX] Iniciando preparación de platos...")
    time.sleep(2)  # Simula cocinar
    
    # Enviar mensaje a otro nodo (latencia de red)
    try:
        sock = socket.socket()
        sock.connect(('guadalajara.server', 5001))
        sock.send(b"CDMX: Platos listos")
        sock.close()
        print("[CDMX] Mensaje enviado con latencia δ₁₂")
    except:
        print("[CDMX] No se pudo conectar (simula fallo de red)")

def nodo_guadalajara(puerto=5001):
    """Nodo 2: Prepara ensaladas"""
    print("[GDL] Iniciando preparación de ensaladas...")
    time.sleep(2)
    print("[GDL] Ensaladas listas")
    
    # Este nodo opera independientemente
    # Si falla CDMX, GDL continúa funcionando

# Simular ejecución distribuida (en realidad estarían en máquinas separadas)
if __name__ == "__main__":
    # Crear procesos que simularían nodos distintos
    p1 = Process(target=nodo_cdmx)
    p2 = Process(target=nodo_guadalajara)
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
```

**Keywords Python:**
- `socket`: Módulo para comunicación de red
- `.connect()`: Conectar a otro nodo (con latencia de red)
- `.send()`: Enviar datos por red

### 8.4 Analogía del Mundo Real

**Escenario:** Red de tres restaurantes preparando un banquete coordinado.

**Nodos físicos:**
- N₁: Restaurante en CDMX (cocina completa independiente)
- N₂: Restaurante en Guadalajara
- N₃: Restaurante en Monterrey

**Tarea distribuida:** Banquete de 300 personas en Querétaro

**Subtareas:**
- τ₁: N₁ prepara 100 platos principales
- τ₂: N₂ prepara 100 ensaladas
- τ₃: N₃ prepara 100 postres

**Ejecución distribuida:**

```
[0:00-2:00] → Los 3 restaurantes cocinan SIMULTÁNEAMENTE
              (ejecución paralela Y distribuida)

[2:00-2:05] → N₁ envía mensaje a N₂: "Platos listos"
              (latencia δ₁₂ por llamada telefónica)

[2:00-4:00] → Transporte físico a Querétaro
              (latencia física enorme, horas)

[4:00] → Sincronización en punto de reunión
```

**Propiedades del sistema distribuido:**

1. **Separación física:** Cientos de kilómetros
2. **Latencia de comunicación:** Llamadas tardan segundos/minutos
3. **Sin memoria compartida:** Cada cocina tiene ingredientes propios
4. **Fallos independientes:** Si N₂ pierde luz, N₁ y N₃ continúan
5. **Paralelismo implícito:** Las tres cocinas trabajan simultáneamente

---

## 9. Tabla Comparativa Formal

| Modelo | P | Solapamiento temporal | exec(τᵢ) ∩ exec(τⱼ) | wait(τᵢ) ≠ ∅ | Ubicación |
|--------|---|---------------------|---------------------|--------------|-----------|
| **Secuencial** | 1 | No | ∅ | — | Single |
| **Asíncrono no concurrente** | 1 | Sí (vía wait) | ∅ | Sí | Single |
| **Concurrente** | ≥1 | Sí | No especifica | No especifica | Variable |
| **Concurrente no asíncrono** | 1 | Sí | ∅ | No | Single |
| **Asíncrono y concurrente** | 1 | Sí | ∅ | Sí | Single |
| **Paralelo** | ≥2 | Sí | ≠ ∅ | No especifica | Single/Multiple |
| **Distribuido** | ≥2 | Sí | ≠ ∅ | No especifica | Multiple (con δᵢⱼ) |

---

## 10. Jerarquía de Inclusión

```
┌─────────────────────────────────────────┐
│            CONCURRENTE                  │
│  (solapamiento temporal de tareas)      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │         PARALELO                  │ │
│  │  (ejecución simultánea física)    │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │      DISTRIBUIDO            │ │ │
│  │  │  (nodos físicamente         │ │ │
│  │  │   separados con latencia)   │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  CONCURRENTE + ASÍNCRONO          │ │
│  │  (solapamiento + wait states)     │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘

         Secuencial (caso especial: sin solapamiento)
```

**Relaciones formales:**
- Distribuido ⊂ Paralelo ⊂ Concurrente
- Asíncrono es ortogonal (puede combinarse con cualquiera)
- Secuencial es el caso degenerado de concurrencia

---

## 11. Resumen de Conceptos Clave

### ¿Cuándo usar cada modelo?

**Secuencial:**
- Scripts simples
- Tareas que deben ejecutarse en orden estricto
- Procesamiento simple sin I/O

**Asíncrono no concurrente:**
- Aplicaciones web (servidor Node.js)
- Programas con mucho I/O (lectura de archivos, red)
- Un solo hilo manejando múltiples conexiones

**Concurrente no asíncrono:**
- Sistemas operativos (time-sharing)
- Interfaces gráficas (UI thread + background tasks)
- Múltiples tareas CPU-bound en una CPU

**Asíncrono y concurrente:**
- Servidores web modernos (Python asyncio, JavaScript async/await)
- Aplicaciones que mezclan I/O y procesamiento
- Máximo aprovechamiento de una CPU

**Paralelo:**
- Procesamiento de datos masivos
- Renderizado de video/3D
- Cálculos científicos
- Machine learning

**Distribuido:**
- Servicios web a gran escala (Google, Facebook)
- Blockchain
- Computación en la nube
- Big Data (Hadoop, Spark)