"""
Ejemplos de Código: Modelos de Ejecución Computacional
=======================================================

Este script contiene ejemplos prácticos de los diferentes modelos de ejecución
estudiados en README_v4.md e implementados en README_codigo.md.

Modelos cubiertos:
1. Secuencial
2. Asíncrono no concurrente
3. Concurrente no asíncrono (threading)
4. Asíncrono concurrente (asyncio)
5. Paralelo (multiprocessing)
"""

import asyncio
import threading
import time
import multiprocessing
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# ============================================================================
# Utilidades
# ============================================================================


def tiempo():
    """Retorna timestamp legible: HH:MM:SS.mmm"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def simular_trabajo_cpu(duracion, nombre):
    """Simula trabajo CPU-bound bloqueante"""
    print(f"[{tiempo()}] {nombre}: INICIO trabajo CPU ({duracion}s)")
    time.sleep(duracion)  # Simula cálculo pesado
    print(f"[{tiempo()}] {nombre}: FIN trabajo CPU")
    return f"Resultado {nombre}"


# ============================================================================
# 1. SECUENCIAL
# ============================================================================


def ejemplo_secuencial():
    """
    Modelo: Secuencial
    - Una tarea termina completamente antes de que la siguiente inicie
    - No hay solapamiento temporal
    - Tiempo total = suma de todos los tiempos
    """
    print("\n" + "=" * 60)
    print("1. EJEMPLO SECUENCIAL")
    print("=" * 60)

    print(f"[{tiempo()}] Inicio secuencial")

    # Tarea 1
    simular_trabajo_cpu(1, "Tarea A")

    # Tarea 2 (solo inicia después de que A termine)
    simular_trabajo_cpu(1, "Tarea B")

    # Tarea 3 (solo inicia después de que B termine)
    simular_trabajo_cpu(1, "Tarea C")

    print(f"[{tiempo()}] Fin secuencial")
    print("Tiempo total: ~3 segundos (suma de todas las tareas)\n")


# ============================================================================
# 2. ASÍNCRONO NO CONCURRENTE
# ============================================================================


async def tarea_async(nombre, duracion):
    """Tarea asíncrona con espera"""
    print(f"[{tiempo()}] {nombre}: INICIO")
    await asyncio.sleep(duracion)  # Espera asíncrona (wait)
    print(f"[{tiempo()}] {nombre}: FIN")
    return f"Resultado {nombre}"


async def ejemplo_asincrono_no_concurrente():
    """
    Modelo: Asíncrono NO concurrente
    - Hay esperas (wait) pero NO se aprovechan
    - Una tarea termina antes de que la siguiente inicie
    - CPU ociosa durante waits
    - Tiempo total = suma de todos los tiempos
    """
    print("\n" + "=" * 60)
    print("2. EJEMPLO ASÍNCRONO NO CONCURRENTE")
    print("=" * 60)

    print(f"[{tiempo()}] Inicio asíncrono no concurrente")

    # Ejecución secuencial con await
    await tarea_async("Tarea A", 1)  # Espera a que termine completamente
    await tarea_async("Tarea B", 1)  # Solo entonces inicia B
    await tarea_async("Tarea C", 1)  # Solo entonces inicia C

    print(f"[{tiempo()}] Fin asíncrono no concurrente")
    print("Tiempo total: ~3 segundos (no se aprovechan los waits)\n")


# ============================================================================
# 3. CONCURRENTE NO ASÍNCRONO (THREADING)
# ============================================================================


def tarea_thread(nombre, duracion):
    """Tarea para ejecutar en un hilo"""
    print(f"[{tiempo()}] {nombre}: INICIO (Hilo: {threading.current_thread().name})")
    time.sleep(duracion)  # Trabajo bloqueante
    print(f"[{tiempo()}] {nombre}: FIN")
    return f"Resultado {nombre}"


def ejemplo_concurrente_no_asincrono():
    """
    Modelo: Concurrente NO asíncrono
    - Hay solapamiento de vidas de tareas (concurrencia)
    - NO hay esperas reales (wait = ∅) o son bloqueantes
    - Time-slicing del OS alterna entre hilos
    - P=1 (un solo core), sin paralelismo físico
    """
    print("\n" + "=" * 60)
    print("3. EJEMPLO CONCURRENTE NO ASÍNCRONO (THREADING)")
    print("=" * 60)

    print(f"[{tiempo()}] Inicio concurrente no asíncrono")

    # Crear múltiples hilos
    hilos = []
    for i, nombre in enumerate(["Tarea A", "Tarea B", "Tarea C"], 1):
        hilo = threading.Thread(target=tarea_thread, args=(nombre, 1))
        hilo.start()
        hilos.append(hilo)

    # Esperar a que todos terminen
    for hilo in hilos:
        hilo.join()

    print(f"[{tiempo()}] Fin concurrente no asíncrono")
    print("Tiempo total: ~1 segundo (concurrencia por time-slicing)\n")


# ============================================================================
# 4. ASÍNCRONO CONCURRENTE (ASYNCIO)
# ============================================================================


async def ejemplo_asincrono_concurrente_gather():
    """
    Modelo: Asíncrono y concurrente
    - Hay esperas (wait) Y se aprovechan
    - Hay solapamiento de vidas de tareas
    - Event loop alterna entre tareas durante waits
    - P=1 (un solo hilo), sin paralelismo físico
    - Tiempo total ≈ max(tiempo de cada tarea)
    """
    print("\n" + "=" * 60)
    print("4. EJEMPLO ASÍNCRONO CONCURRENTE (ASYNCIO.GATHER)")
    print("=" * 60)

    print(f"[{tiempo()}] Inicio asíncrono concurrente")

    # Ejecutar múltiples tareas concurrentemente
    resultados = await asyncio.gather(
        tarea_async("Tarea A", 1), tarea_async("Tarea B", 1), tarea_async("Tarea C", 1)
    )

    print(f"[{tiempo()}] Fin asíncrono concurrente")
    print(f"Resultados: {resultados}")
    print("Tiempo total: ~1 segundo (aprovecha waits simultáneos)\n")


async def ejemplo_asincrono_concurrente_create_task():
    """
    Ejemplo con create_task: lanzar tareas y continuar con otras cosas
    """
    print("\n" + "=" * 60)
    print("4b. EJEMPLO ASYNCIO.CREATE_TASK")
    print("=" * 60)

    print(f"[{tiempo()}] Main: inicio")

    # Lanzar tareas en background (no esperamos inmediatamente)
    task_a = asyncio.create_task(tarea_async("Tarea A", 2))
    task_b = asyncio.create_task(tarea_async("Tarea B", 1))

    # Hacer otras cosas mientras las tareas corren
    print(f"[{tiempo()}] Main: tareas lanzadas, haciendo otra cosa...")
    await asyncio.sleep(0.5)
    print(f"[{tiempo()}] Main: terminé mi trabajo")

    # Ahora sí esperamos los resultados
    print(f"[{tiempo()}] Main: esperando resultados...")
    resultado_a = await task_a
    resultado_b = await task_b

    print(f"[{tiempo()}] Main: fin - resultados: {resultado_a}, {resultado_b}\n")


async def ejemplo_asincrono_concurrente_wait():
    """
    Ejemplo con asyncio.wait: control avanzado sobre múltiples tareas
    """
    print("\n" + "=" * 60)
    print("4c. EJEMPLO ASYNCIO.WAIT (FIRST_COMPLETED)")
    print("=" * 60)

    # Crear tareas con diferentes duraciones
    task_a = asyncio.create_task(tarea_async("Tarea A", 1))
    task_b = asyncio.create_task(tarea_async("Tarea B", 2))
    task_c = asyncio.create_task(tarea_async("Tarea C", 3))

    # Esperar hasta que la primera termine
    done, pending = await asyncio.wait(
        {task_a, task_b, task_c}, return_when=asyncio.FIRST_COMPLETED
    )

    print(f"[{tiempo()}] Primera tarea completada: {[t.result() for t in done]}")
    print(f"[{tiempo()}] Tareas pendientes: {len(pending)}")

    # Cancelar las pendientes
    for task in pending:
        task.cancel()

    print()


# ============================================================================
# 5. PARALELO (MULTIPROCESSING)
# ============================================================================


def tarea_paralela(nombre, duracion):
    """Tarea para ejecutar en un proceso separado"""
    print(
        f"[{tiempo()}] {nombre}: INICIO (Proceso: {multiprocessing.current_process().name})"
    )
    time.sleep(duracion)  # Trabajo CPU-bound simulado
    print(f"[{tiempo()}] {nombre}: FIN")
    return f"Resultado {nombre}"


def ejemplo_paralelo_multiprocessing():
    """
    Modelo: Paralelo
    - Ejecución simultánea física en múltiples cores
    - P ≥ 2 (múltiples procesadores)
    - Speedup real: hasta P veces más rápido
    """
    print("\n" + "=" * 60)
    print("5. EJEMPLO PARALELO (MULTIPROCESSING)")
    print("=" * 60)

    print(f"[{tiempo()}] Inicio paralelo")
    print(f"Cores disponibles: {multiprocessing.cpu_count()}")

    # Crear múltiples procesos
    procesos = []
    for i, nombre in enumerate(["Tarea A", "Tarea B", "Tarea C"], 1):
        proceso = multiprocessing.Process(target=tarea_paralela, args=(nombre, 1))
        proceso.start()
        procesos.append(proceso)

    # Esperar a que todos terminen
    for proceso in procesos:
        proceso.join()

    print(f"[{tiempo()}] Fin paralelo")
    print("Tiempo total: ~1 segundo (ejecución simultánea en múltiples cores)\n")


def ejemplo_paralelo_processpool():
    """
    Ejemplo con ProcessPoolExecutor: más control y mejor para tareas repetitivas
    """
    print("\n" + "=" * 60)
    print("5b. EJEMPLO PARALELO (PROCESSPOOLEXECUTOR)")
    print("=" * 60)

    print(f"[{tiempo()}] Inicio ProcessPoolExecutor")

    # Usar ProcessPoolExecutor para tareas paralelas
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Enviar tareas al pool
        futures = [
            executor.submit(tarea_paralela, f"Tarea {chr(65+i)}", 1) for i in range(3)
        ]

        # Recoger resultados
        resultados = [future.result() for future in futures]

    print(f"[{tiempo()}] Fin ProcessPoolExecutor")
    print(f"Resultados: {resultados}\n")


# ============================================================================
# 6. COMPARACIÓN: ASYNCIO VS THREADING
# ============================================================================


async def descargar_async(url_id):
    """Simula descarga asíncrona"""
    await asyncio.sleep(0.5)  # Simula latencia de red
    return f"Datos de URL {url_id}"


def descargar_thread(url_id):
    """Simula descarga con threading"""
    time.sleep(0.5)  # Simula latencia de red
    return f"Datos de URL {url_id}"


async def ejemplo_comparacion_asyncio():
    """Comparación: asyncio para I/O-bound"""
    print("\n" + "=" * 60)
    print("6. COMPARACIÓN: ASYNCIO PARA I/O-BOUND")
    print("=" * 60)

    inicio = time.time()
    print(f"[{tiempo()}] Asyncio: inicio")

    # Descargar 10 URLs concurrentemente
    tareas = [descargar_async(i) for i in range(10)]
    resultados = await asyncio.gather(*tareas)

    tiempo_total = time.time() - inicio
    print(f"[{tiempo()}] Asyncio: fin")
    print(f"Tiempo total: {tiempo_total:.2f}s (aprovecha I/O waits)\n")


def ejemplo_comparacion_threading():
    """Comparación: threading para I/O-bound"""
    print("\n" + "=" * 60)
    print("6b. COMPARACIÓN: THREADING PARA I/O-BOUND")
    print("=" * 60)

    inicio = time.time()
    print(f"[{tiempo()}] Threading: inicio")

    # Descargar 10 URLs con threading
    hilos = []
    resultados = []

    def worker(url_id):
        resultado = descargar_thread(url_id)
        resultados.append(resultado)

    for i in range(10):
        hilo = threading.Thread(target=worker, args=(i,))
        hilo.start()
        hilos.append(hilo)

    for hilo in hilos:
        hilo.join()

    tiempo_total = time.time() - inicio
    print(f"[{tiempo()}] Threading: fin")
    print(f"Tiempo total: {tiempo_total:.2f}s\n")


# ============================================================================
# 7. CASO ESPECIAL: TRABAJO CPU-BOUND EN ASYNCIO
# ============================================================================


async def ejemplo_cpu_bound_en_asyncio():
    """
    Demostración: asyncio NO ayuda con trabajo CPU-bound
    El event loop se bloquea si no hay await
    """
    print("\n" + "=" * 60)
    print("7. CASO ESPECIAL: CPU-BOUND EN ASYNCIO (NO RECOMENDADO)")
    print("=" * 60)

    async def tarea_cpu_mala():
        print(f"[{tiempo()}] Tarea CPU: INICIO")
        # Trabajo CPU bloqueante (NO usa await)
        resultado = sum(range(10_000_000))  # Bloquea el event loop
        print(f"[{tiempo()}] Tarea CPU: FIN")
        return resultado

    async def tarea_io():
        print(f"[{tiempo()}] Tarea I/O: INICIO")
        await asyncio.sleep(1)  # Esta tarea NO puede ejecutar mientras CPU bloquea
        print(f"[{tiempo()}] Tarea I/O: FIN")

    inicio = time.time()
    await asyncio.gather(tarea_cpu_mala(), tarea_io())
    tiempo_total = time.time() - inicio

    print(f"Tiempo total: {tiempo_total:.2f}s")
    print("⚠️  Problema: tarea_io no puede ejecutar hasta que tarea_cpu_mala termine")
    print("⚠️  Solución: usar ProcessPoolExecutor para CPU-bound\n")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================


def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "=" * 60)
    print("EJEMPLOS DE MODELOS DE EJECUCIÓN COMPUTACIONAL")
    print("=" * 60)

    # 1. Secuencial
    ejemplo_secuencial()
    time.sleep(0.5)

    # 2. Asíncrono no concurrente
    asyncio.run(ejemplo_asincrono_no_concurrente())
    time.sleep(0.5)

    # 3. Concurrente no asíncrono
    ejemplo_concurrente_no_asincrono()
    time.sleep(0.5)

    # 4. Asíncrono concurrente
    asyncio.run(ejemplo_asincrono_concurrente_gather())
    time.sleep(0.5)

    asyncio.run(ejemplo_asincrono_concurrente_create_task())
    time.sleep(0.5)

    asyncio.run(ejemplo_asincrono_concurrente_wait())
    time.sleep(0.5)

    # 5. Paralelo
    ejemplo_paralelo_multiprocessing()
    time.sleep(0.5)

    ejemplo_paralelo_processpool()
    time.sleep(0.5)

    # 6. Comparaciones
    asyncio.run(ejemplo_comparacion_asyncio())
    time.sleep(0.5)

    ejemplo_comparacion_threading()
    time.sleep(0.5)

    # 7. Caso especial
    asyncio.run(ejemplo_cpu_bound_en_asyncio())

    print("\n" + "=" * 60)
    print("FIN DE EJEMPLOS")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
