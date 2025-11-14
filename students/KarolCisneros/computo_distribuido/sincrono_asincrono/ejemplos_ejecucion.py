"""
Ejemplos de Modelos de Ejecución Computacional
==============================================

Este script implementa ejemplos prácticos de los modelos matemáticos formales
descritos en README_v4.md y README_codigo.md:

1. SECUENCIAL - Tareas ejecutan una después de otra
2. ASÍNCRONO NO CONCURRENTE - Hay waits pero no se aprovechan
3. CONCURRENTE NO ASÍNCRONO - Time-slicing sin waits reales
4. ASÍNCRONO Y CONCURRENTE - Aprovecha waits con event loop
5. PARALELO - Ejecución simultánea física en múltiples cores

Autor: Basado en el framework matemático formal del curso
"""

import asyncio
import threading
import time
import multiprocessing
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# ============================================================================
# UTILIDADES
# ============================================================================


def tiempo():
    """Retorna timestamp legible: HH:MM:SS.mmm"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def trabajo_cpu(duracion, nombre):
    """Simula trabajo CPU-bound (cálculo intensivo)"""
    print(f"[{tiempo()}] {nombre}: INICIO trabajo CPU ({duracion}s)")
    inicio = time.time()
    # Simula cálculo pesado
    while time.time() - inicio < duracion:
        sum(range(10000))  # Trabajo CPU
    print(f"[{tiempo()}] {nombre}: FIN trabajo CPU")


def trabajo_io(duracion, nombre):
    """Simula trabajo I/O-bound (espera de dispositivo/red)"""
    print(f"[{tiempo()}] {nombre}: INICIO espera I/O ({duracion}s)")
    time.sleep(duracion)  # Simula lectura de disco, red, etc.
    print(f"[{tiempo()}] {nombre}: FIN espera I/O")


# ============================================================================
# 1. MODELO SECUENCIAL
# ============================================================================


def ejemplo_secuencial():
    """
    Modelo: SECUENCIAL
    Propiedades:
    - ∀ i≠j: end(τᵢ) ≤ start(τⱼ) OR end(τⱼ) ≤ start(τᵢ)
    - |ExecutingAt(t)| = 1 siempre
    - Tiempo total = suma de todos los tiempos
    """
    print("\n" + "=" * 70)
    print("1. MODELO SECUENCIAL")
    print("=" * 70)
    print("Tareas ejecutan una después de otra, sin solapamiento")

    print(f"\n[{tiempo()}] Inicio secuencial")

    # Tarea 1: Preparar café
    trabajo_io(1, "Preparar café")

    # Tarea 2: Tostar pan
    trabajo_io(1, "Tostar pan")

    # Tarea 3: Cortar fruta
    trabajo_cpu(0.5, "Cortar fruta")

    print(f"[{tiempo()}] Fin secuencial")
    print("Tiempo total: ~2.5 segundos (suma de todas las tareas)")


# ============================================================================
# 2. ASÍNCRONO NO CONCURRENTE
# ============================================================================


async def tarea_asincrona(nombre, duracion):
    """Tarea asíncrona que simula I/O"""
    print(f"[{tiempo()}] {nombre}: INICIO")
    await asyncio.sleep(duracion)  # Simula espera I/O
    print(f"[{tiempo()}] {nombre}: FIN")
    return f"Resultado {nombre}"


async def ejemplo_asincrono_no_concurrente():
    """
    Modelo: ASÍNCRONO NO CONCURRENTE
    Propiedades:
    - ∃ τ: wait(τ) ≠ ∅ (hay esperas reales)
    - ∀ i≠j: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] = ∅ (no hay concurrencia)
    - CPU ociosa durante waits (no se aprovechan)
    """
    print("\n" + "=" * 70)
    print("2. ASÍNCRONO NO CONCURRENTE")
    print("=" * 70)
    print("Hay waits pero NO se aprovechan - CPU ociosa durante esperas")

    print(f"\n[{tiempo()}] Inicio asíncrono no concurrente")

    # Ejecución secuencial con await
    await tarea_asincrona("Cafetera", 1)
    await tarea_asincrona("Tostadora", 1)

    print(f"[{tiempo()}] Fin asíncrono no concurrente")
    print("Tiempo total: ~2 segundos (igual que secuencial)")
    print("⚠️  Nota: La CPU está ociosa durante los awaits")


# ============================================================================
# 3. CONCURRENTE NO ASÍNCRONO (THREADING)
# ============================================================================


def tarea_threading(nombre, duracion):
    """Tarea para ejecutar en un hilo"""
    print(f"[{tiempo()}] {nombre}: INICIO (Hilo: {threading.current_thread().name})")
    trabajo_cpu(duracion, nombre)
    print(f"[{tiempo()}] {nombre}: FIN")


def ejemplo_concurrente_no_asincrono():
    """
    Modelo: CONCURRENTE NO ASÍNCRONO
    Propiedades:
    - ∃ i≠j: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅ (hay concurrencia)
    - ∀ τ: wait(τ) = ∅ (no hay esperas reales, solo time-slicing)
    - P=1 (sin paralelismo físico)
    - Alternancia por time-slicing del OS
    """
    print("\n" + "=" * 70)
    print("3. CONCURRENTE NO ASÍNCRONO (THREADING)")
    print("=" * 70)
    print("Time-slicing entre hilos - NO hay waits reales")

    print(f"\n[{tiempo()}] Inicio concurrente no asíncrono")
    print(f"Cores disponibles: {multiprocessing.cpu_count()}")

    # Crear múltiples hilos
    hilos = []
    for i, (nombre, duracion) in enumerate(
        [("Risotto", 0.5), ("Salsa", 0.5), ("Vegetales", 0.5)]
    ):
        hilo = threading.Thread(
            target=tarea_threading, args=(nombre, duracion), name=f"Thread-{i+1}"
        )
        hilos.append(hilo)
        hilo.start()

    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()

    print(f"[{tiempo()}] Fin concurrente no asíncrono")
    print("⚠️  Nota: En Python, GIL limita el paralelismo real")
    print("⚠️  Nota: Las tareas alternan por time-slicing del OS")


# ============================================================================
# 4. ASÍNCRONO Y CONCURRENTE (ASYNCIO)
# ============================================================================


async def ejemplo_asincrono_concurrente_gather():
    """
    Modelo: ASÍNCRONO Y CONCURRENTE (con gather)
    Propiedades:
    - ∃ i≠j: [start(τᵢ), end(τᵢ)] ∩ [start(τⱼ), end(τⱼ)] ≠ ∅ (concurrencia)
    - ∃ τ: wait(τ) ≠ ∅ (asincronía)
    - ∃ i,j: exec(τⱼ) ∩ wait(τᵢ) ≠ ∅ (aprovecha waits)
    - P=1 (sin paralelismo físico)
    """
    print("\n" + "=" * 70)
    print("4. ASÍNCRONO Y CONCURRENTE (gather)")
    print("=" * 70)
    print("Aprovecha waits - múltiples tareas concurrentes")

    print(f"\n[{tiempo()}] Inicio asíncrono concurrente")

    # Ejecutar múltiples tareas concurrentemente
    resultados = await asyncio.gather(
        tarea_asincrona("Cafetera", 2),
        tarea_asincrona("Tostadora", 1),
        tarea_asincrona("Cortar fruta", 1.5),
    )

    print(f"[{tiempo()}] Fin asíncrono concurrente")
    print(f"Resultados: {resultados}")
    print("Tiempo total: ~2 segundos (máximo, no suma)")
    print("✅ Se aprovechan los waits - mejor rendimiento")


async def ejemplo_asincrono_concurrente_create_task():
    """
    Modelo: ASÍNCRONO Y CONCURRENTE (con create_task)
    Similar a gather pero con control más fino
    """
    print("\n" + "=" * 70)
    print("4b. ASÍNCRONO Y CONCURRENTE (create_task)")
    print("=" * 70)
    print("Lanza tareas y continúa ejecutando código")

    print(f"\n[{tiempo()}] Inicio create_task")

    # Lanzar tareas sin esperar inmediatamente
    task_a = asyncio.create_task(tarea_asincrona("Tarea A", 2))
    task_b = asyncio.create_task(tarea_asincrona("Tarea B", 1))

    print(f"[{tiempo()}] Tareas lanzadas, haciendo otra cosa...")

    # Mientras tanto, hacer otra cosa
    await asyncio.sleep(0.5)
    print(f"[{tiempo()}] Terminé mi trabajo, esperando resultados...")

    # Ahora sí esperar los resultados
    resultado_a = await task_a
    resultado_b = await task_b

    print(f"[{tiempo()}] Fin create_task")
    print(f"Resultados: {resultado_a}, {resultado_b}")
    print("✅ Pudimos hacer trabajo adicional mientras las tareas corrían")


async def ejemplo_trabajo_cpu_en_async():
    """
    Ejemplo que muestra el problema de trabajo CPU-bound en async
    """
    print("\n" + "=" * 70)
    print("4c. PROBLEMA: Trabajo CPU-bound en async")
    print("=" * 70)
    print("⚠️  Trabajo CPU bloquea el event loop")

    async def tarea_con_cpu(nombre, duracion_cpu, duracion_io):
        print(f"[{tiempo()}] {nombre}: INICIO")
        # Trabajo CPU ANTES del await (bloquea el event loop)
        trabajo_cpu(duracion_cpu, nombre)
        print(f"[{tiempo()}] {nombre}: llegó al await")
        # Ahora sí hace await (puede cambiar de tarea)
        await asyncio.sleep(duracion_io)
        print(f"[{tiempo()}] {nombre}: FIN")

    print(f"\n[{tiempo()}] Inicio ejemplo CPU en async")

    await asyncio.gather(
        tarea_con_cpu("Tarea A", 0.5, 1), tarea_con_cpu("Tarea B", 0.3, 1)
    )

    print(f"[{tiempo()}] Fin ejemplo CPU en async")
    print("⚠️  Observa: El trabajo CPU se ejecuta secuencialmente")
    print("⚠️  Solo los awaits se ejecutan concurrentemente")


# ============================================================================
# 5. PARALELO (MULTIPROCESSING)
# ============================================================================


def tarea_paralela(nombre, duracion):
    """Tarea para ejecutar en proceso separado"""
    print(f"[{tiempo()}] {nombre}: INICIO (Proceso: {os.getpid()})")
    trabajo_cpu(duracion, nombre)
    print(f"[{tiempo()}] {nombre}: FIN")
    return f"Resultado {nombre}"


def ejemplo_paralelo_multiprocessing():
    """
    Modelo: PARALELO
    Propiedades:
    - ∃ i≠j, ∃ t: (t ∈ exec(τᵢ)) AND (t ∈ exec(τⱼ)) (ejecución simultánea física)
    - P ≥ 2 (múltiples cores)
    - |ExecutingAt(t)| ≥ 2 en algunos instantes
    """

    print("\n" + "=" * 70)
    print("5. PARALELO (MULTIPROCESSING)")
    print("=" * 70)
    print("Ejecución simultánea física en múltiples cores")

    print(f"\n[{tiempo()}] Inicio paralelo")
    print(f"Cores disponibles: {multiprocessing.cpu_count()}")

    # Crear múltiples procesos
    procesos = []
    for nombre, duracion in [("Tarea A", 1), ("Tarea B", 1), ("Tarea C", 1)]:
        proceso = multiprocessing.Process(
            target=tarea_paralela, args=(nombre, duracion)
        )
        procesos.append(proceso)
        proceso.start()

    # Esperar a que todos terminen
    for proceso in procesos:
        proceso.join()

    print(f"[{tiempo()}] Fin paralelo")
    print("✅ Tareas ejecutan simultáneamente en diferentes cores")
    print("✅ Speedup real para trabajo CPU-bound")


def ejemplo_paralelo_process_pool():
    """
    Ejemplo usando ProcessPoolExecutor (más fácil de usar)
    """
    print("\n" + "=" * 70)
    print("5b. PARALELO (ProcessPoolExecutor)")
    print("=" * 70)

    def tarea_cpu_intensiva(nombre):
        """Tarea CPU-bound intensiva"""
        print(f"[{tiempo()}] {nombre}: INICIO")
        resultado = sum(range(1000000))  # Trabajo CPU
        print(f"[{tiempo()}] {nombre}: FIN")
        return f"Resultado {nombre}: {resultado % 1000}"

    print(f"\n[{tiempo()}] Inicio ProcessPoolExecutor")

    with ProcessPoolExecutor(max_workers=3) as executor:
        # Enviar tareas al pool
        futures = [executor.submit(tarea_cpu_intensiva, f"Tarea {i}") for i in range(3)]

        # Recoger resultados
        resultados = [fut.result() for fut in futures]

    print(f"[{tiempo()}] Fin ProcessPoolExecutor")
    print(f"Resultados: {resultados}")
    print("✅ Trabajo CPU distribuido en múltiples procesos")


# ============================================================================
# 6. COMPARACIÓN: ASYNCIO vs THREADING vs MULTIPROCESSING
# ============================================================================


async def ejemplo_comparacion():
    """
    Comparación directa de los tres enfoques principales
    """
    print("\n" + "=" * 70)
    print("6. COMPARACIÓN: ASYNCIO vs THREADING vs MULTIPROCESSING")
    print("=" * 70)

    def tarea_io_threading(nombre, duracion):
        print(f"[{tiempo()}] Threading {nombre}: INICIO")
        time.sleep(duracion)
        print(f"[{tiempo()}] Threading {nombre}: FIN")

    async def tarea_io_asyncio(nombre, duracion):
        print(f"[{tiempo()}] Asyncio {nombre}: INICIO")
        await asyncio.sleep(duracion)
        print(f"[{tiempo()}] Asyncio {nombre}: FIN")

    def tarea_io_multiprocessing(nombre, duracion):
        print(f"[{tiempo()}] Multiprocessing {nombre}: INICIO")
        time.sleep(duracion)
        print(f"[{tiempo()}] Multiprocessing {nombre}: FIN")

    print("\n--- THREADING (concurrente no asíncrono) ---")
    inicio = time.time()
    hilos = [
        threading.Thread(target=tarea_io_threading, args=(f"Tarea {i}", 1))
        for i in range(3)
    ]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
    tiempo_threading = time.time() - inicio
    print(f"Tiempo threading: {tiempo_threading:.2f}s")

    print("\n--- ASYNCIO (asíncrono y concurrente) ---")
    inicio = time.time()
    await asyncio.gather(*[tarea_io_asyncio(f"Tarea {i}", 1) for i in range(3)])
    tiempo_asyncio = time.time() - inicio
    print(f"Tiempo asyncio: {tiempo_asyncio:.2f}s")

    print("\n--- MULTIPROCESSING (paralelo) ---")
    inicio = time.time()
    procesos = [
        multiprocessing.Process(target=tarea_io_multiprocessing, args=(f"Tarea {i}", 1))
        for i in range(3)
    ]
    for proceso in procesos:
        proceso.start()
    for proceso in procesos:
        proceso.join()
    tiempo_multiprocessing = time.time() - inicio
    print(f"Tiempo multiprocessing: {tiempo_multiprocessing:.2f}s")

    print("\n" + "-" * 70)
    print("RESUMEN:")
    print(f"  Threading:    {tiempo_threading:.2f}s (time-slicing, GIL limita)")
    print(f"  Asyncio:      {tiempo_asyncio:.2f}s (event loop, aprovecha waits)")
    print(f"  Multiprocessing: {tiempo_multiprocessing:.2f}s (paralelismo real)")
    print("-" * 70)


# ============================================================================
# 7. EJEMPLOS AVANZADOS
# ============================================================================


async def ejemplo_avanzado_wait():
    """
    Ejemplo usando asyncio.wait() para control fino
    """
    print("\n" + "=" * 70)
    print("7. EJEMPLO AVANZADO: asyncio.wait()")
    print("=" * 70)
    print("Esperar hasta que la primera tarea termine")

    async def tarea(nombre, duracion):
        print(f"[{tiempo()}] {nombre}: INICIO")
        await asyncio.sleep(duracion)
        print(f"[{tiempo()}] {nombre}: FIN")
        return f"Resultado {nombre}"

    print(f"\n[{tiempo()}] Inicio wait()")

    # Crear tareas
    tasks = {
        asyncio.create_task(tarea("Rápida", 1)),
        asyncio.create_task(tarea("Media", 2)),
        asyncio.create_task(tarea("Lenta", 3)),
    }

    # Esperar hasta que la primera termine
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    print(f"[{tiempo()}] Primera tarea completada: {[t.result() for t in done]}")
    print(f"[{tiempo()}] Tareas pendientes: {len(pending)}")

    # Cancelar las pendientes
    for task in pending:
        task.cancel()

    print(f"[{tiempo()}] Fin wait()")


async def ejemplo_avanzado_timeout():
    """
    Ejemplo con timeout usando asyncio.wait_for()
    """
    print("\n" + "=" * 70)
    print("7b. EJEMPLO AVANZADO: Timeout")
    print("=" * 70)

    async def tarea_lenta(duracion):
        print(f"[{tiempo()}] Tarea lenta: INICIO ({duracion}s)")
        await asyncio.sleep(duracion)
        print(f"[{tiempo()}] Tarea lenta: FIN")
        return "Completada"

    print(f"\n[{tiempo()}] Inicio timeout")

    try:
        # Esperar máximo 2 segundos
        resultado = await asyncio.wait_for(tarea_lenta(5), timeout=2.0)
        print(f"Resultado: {resultado}")
    except asyncio.TimeoutError:
        print(f"[{tiempo()}] ⚠️  Timeout: La tarea tardó más de 2 segundos")

    print(f"[{tiempo()}] Fin timeout")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================


def main():
    """
    Ejecuta todos los ejemplos
    """
    print("\n" + "=" * 70)
    print("EJEMPLOS DE MODELOS DE EJECUCIÓN COMPUTACIONAL")
    print("=" * 70)
    print("\nEste script demuestra los diferentes modelos de ejecución:")
    print("1. Secuencial")
    print("2. Asíncrono no concurrente")
    print("3. Concurrente no asíncrono (threading)")
    print("4. Asíncrono y concurrente (asyncio)")
    print("5. Paralelo (multiprocessing)")
    print("6. Comparación")
    print("7. Ejemplos avanzados")

    # Ejecutar ejemplos secuenciales
    ejemplo_secuencial()

    # Ejecutar ejemplos asíncronos
    asyncio.run(ejemplo_asincrono_no_concurrente())
    asyncio.run(ejemplo_asincrono_concurrente_gather())
    asyncio.run(ejemplo_asincrono_concurrente_create_task())
    asyncio.run(ejemplo_trabajo_cpu_en_async())

    # Ejecutar ejemplos de threading
    ejemplo_concurrente_no_asincrono()

    # Ejecutar ejemplos paralelos
    ejemplo_paralelo_multiprocessing()
    ejemplo_paralelo_process_pool()

    # Comparación
    asyncio.run(ejemplo_comparacion())

    # Ejemplos avanzados
    asyncio.run(ejemplo_avanzado_wait())
    asyncio.run(ejemplo_avanzado_timeout())

    print("\n" + "=" * 70)
    print("FIN DE EJEMPLOS")
    print("=" * 70)
    print("\nReferencias:")
    print("- README_v4.md: Framework matemático formal")
    print("- README_codigo.md: Guía de implementación en Python")


if __name__ == "__main__":
    main()
