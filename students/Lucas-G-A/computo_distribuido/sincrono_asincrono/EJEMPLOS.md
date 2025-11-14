# Guía de Ejemplos de Código

Este documento explica los ejemplos en `codigo_v2.py` y cómo ejecutarlos.

## Requisitos

No se requieren dependencias adicionales más allá de la biblioteca estándar de Python:
- `threading`
- `multiprocessing`
- `asyncio`
- `concurrent.futures`

## Cómo Ejecutar

```bash
python codigo_v2.py
```

## Ejemplos Incluidos

### 1. Ejecución Secuencial
**Función:** `ejemplo_secuencial()`

- Ejecuta tareas una después de otra
- No hay concurrencia ni paralelismo
- Tiempo total = suma de tiempos individuales

**Cuándo usar:** Tareas simples que deben ejecutarse en orden.

---

### 2. Hilos (Threads) - I/O-bound
**Función:** `ejemplo_hilos()`

- Usa `threading.Thread` para tareas I/O-bound
- Múltiples hilos comparten la misma memoria
- Ideal para: descargas, lectura de archivos, llamadas HTTP
- **Ventaja:** Mientras un hilo espera I/O, otros pueden avanzar

**Cuándo usar:** Tareas que pasan mucho tiempo esperando (red, disco, base de datos).

---

### 3. Procesos (Processes) - CPU-bound
**Función:** `ejemplo_procesos()`

- Usa `multiprocessing.Process` para tareas CPU-bound
- Cada proceso tiene su propia memoria aislada
- Ideal para: cálculos matemáticos, procesamiento de imágenes
- **Ventaja:** Paralelismo real en múltiples núcleos (evita GIL)

**Cuándo usar:** Tareas que consumen mucha CPU y pueden ejecutarse en paralelo.

---

### 4. Asíncrono (Async/Await)
**Función:** `ejemplo_asincrono()`

- Usa `asyncio` con `async/await`
- Event loop gestiona múltiples tareas concurrentemente
- Ideal para: muchas conexiones I/O simultáneas
- **Ventaja:** Muy eficiente para I/O, bajo overhead

**Cuándo usar:** Servidores web, APIs con muchas conexiones simultáneas.

---

### 5. ThreadPoolExecutor
**Función:** `ejemplo_thread_pool()`

- API de alto nivel para gestionar hilos
- Similar a hilos manuales pero más fácil de usar
- Ideal para: I/O-bound con pool de trabajadores

**Cuándo usar:** Cuando necesitas un pool de hilos reutilizables para I/O.

---

### 6. ProcessPoolExecutor
**Función:** `ejemplo_process_pool()`

- API de alto nivel para gestionar procesos
- Similar a procesos manuales pero más fácil de usar
- Ideal para: CPU-bound con pool de trabajadores

**Cuándo usar:** Cuando necesitas un pool de procesos reutilizables para CPU.

---

### 7. Comparación: GIL con Hilos vs Procesos
**Funciones:** `ejemplo_gil_hilos()`, `ejemplo_gil_procesos()`

- Demuestra el efecto del GIL (Global Interpreter Lock) en Python
- Hilos: GIL limita el paralelismo real para CPU-bound
- Procesos: Cada proceso tiene su propio GIL, permitiendo paralelismo real

**Observación:** Para CPU-bound, los procesos son más rápidos que los hilos.

---

## Tabla de Decisión Rápida

| Tipo de Tarea | Mecanismo Recomendado | Ejemplo |
|---------------|----------------------|---------|
| I/O-bound (red, disco) | `ThreadPoolExecutor` o `asyncio` | Descargar archivos, consultas DB |
| CPU-bound (cálculos) | `ProcessPoolExecutor` | Procesar imágenes, cálculos numéricos |
| Muchas conexiones I/O | `asyncio` | Servidor web, API REST |
| Tareas simples en orden | Secuencial | Scripts simples |

---

## Conceptos Clave

### I/O-bound vs CPU-bound

- **I/O-bound:** El tiempo está dominado por esperas (red, disco, base de datos)
  - Ejemplo: Descargar archivos, leer bases de datos
  - Mejora con: Hilos o asyncio

- **CPU-bound:** El tiempo está dominado por cómputo puro
  - Ejemplo: Cálculos matemáticos, procesamiento de imágenes
  - Mejora con: Procesos (paralelismo real)

### GIL (Global Interpreter Lock)

- En CPython, solo un hilo puede ejecutar bytecode Python a la vez
- **Implicación:** Hilos no dan paralelismo real para CPU-bound
- **Solución:** Usar procesos para CPU-bound (cada proceso tiene su GIL)

### Memoria Compartida

- **Hilos:** Comparten memoria del proceso (fácil comunicación, riesgo de race conditions)
- **Procesos:** Memoria aislada (comunicación por IPC, más seguro)

---

## Notas de Ejecución

- Los ejemplos de procesos están comentados por defecto porque pueden ser más lentos en algunos sistemas
- Descomenta las líneas en `main()` para probar todos los ejemplos
- En sistemas con pocos núcleos, el paralelismo puede no mostrar mejoras significativas
- Los tiempos pueden variar según el hardware

---

## Próximos Pasos

1. Experimenta modificando los parámetros (duración, número de tareas)
2. Compara los tiempos de ejecución entre diferentes métodos
3. Prueba con tareas reales (descargar archivos, procesar imágenes)
4. Lee los README.md para entender la teoría detrás de estos conceptos

