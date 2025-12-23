"""
Ejemplos prácticos de modelos de ejecución computacional
Basado en los conceptos de hilos vs procesos y sincrónico vs asíncrono
"""

import time
import threading
import multiprocessing
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os


# ============================================================================
# 1. SECUENCIAL (Sequential)
# ============================================================================
def tarea_cpu(nombre, duracion=0.1):
    """Simula una tarea que consume CPU"""
    inicio = time.time()
    while time.time() - inicio < duracion:
        sum(range(1000))  # Trabajo CPU
    print(f"[SECUENCIAL] {nombre} completado")


def ejemplo_secuencial():
    """Ejecuta tareas una después de otra"""
    print("\n=== 1. EJECUCIÓN SECUENCIAL ===")
    inicio = time.time()
    tarea_cpu("Tarea 1", 0.2)
    tarea_cpu("Tarea 2", 0.2)
    tarea_cpu("Tarea 3", 0.2)
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s\n")


# ============================================================================
# 2. HILOS (Threads) - I/O-bound
# ============================================================================
def tarea_io(nombre, duracion=0.5):
    """Simula una tarea I/O-bound (espera de red/disco)"""
    print(f"[HILO] {nombre} iniciando...")
    time.sleep(duracion)  # Simula espera de I/O
    print(f"[HILO] {nombre} completado")


def ejemplo_hilos():
    """Usa hilos para tareas I/O-bound concurrentes"""
    print("\n=== 2. HILOS (I/O-bound) ===")
    inicio = time.time()
    
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=tarea_io, args=(f"Tarea {i+1}", 0.5))
        hilos.append(hilo)
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s (vs 1.5s secuencial)\n")


# ============================================================================
# 3. PROCESOS (Processes) - CPU-bound
# ============================================================================
def tarea_cpu_intensiva(nombre, numero):
    """Tarea CPU-bound: calcula la suma de números"""
    resultado = sum(range(numero))
    print(f"[PROCESO] {nombre} completado: suma hasta {numero} = {resultado}")


def ejemplo_procesos():
    """Usa procesos para tareas CPU-bound en paralelo"""
    print("\n=== 3. PROCESOS (CPU-bound) ===")
    inicio = time.time()
    
    procesos = []
    for i in range(3):
        proceso = multiprocessing.Process(
            target=tarea_cpu_intensiva, 
            args=(f"Tarea {i+1}", 1000000)
        )
        procesos.append(proceso)
        proceso.start()
    
    for proceso in procesos:
        proceso.join()
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s\n")


# ============================================================================
# 4. ASÍNCRONO (Async/Await) - Event Loop
# ============================================================================
async def tarea_async(nombre, duracion=0.5):
    """Tarea asíncrona que simula I/O"""
    print(f"[ASYNC] {nombre} iniciando...")
    await asyncio.sleep(duracion)  # Espera no bloqueante
    print(f"[ASYNC] {nombre} completado")


async def ejemplo_asincrono():
    """Ejecuta múltiples tareas asíncronas concurrentemente"""
    print("\n=== 4. ASÍNCRONO (Event Loop) ===")
    inicio = time.time()
    
    # Ejecuta todas las tareas concurrentemente
    await asyncio.gather(
        tarea_async("Tarea 1", 0.5),
        tarea_async("Tarea 2", 0.5),
        tarea_async("Tarea 3", 0.5)
    )
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s (vs 1.5s secuencial)\n")


# ============================================================================
# 5. ThreadPoolExecutor - Para I/O-bound
# ============================================================================
def ejemplo_thread_pool():
    """Usa ThreadPoolExecutor para tareas I/O-bound"""
    print("\n=== 5. ThreadPoolExecutor (I/O-bound) ===")
    inicio = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(tarea_io, f"Tarea {i+1}", 0.5)
            for i in range(3)
        ]
        # Espera a que todas completen
        for future in futures:
            future.result()
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s\n")


# ============================================================================
# 6. ProcessPoolExecutor - Para CPU-bound
# ============================================================================
def ejemplo_process_pool():
    """Usa ProcessPoolExecutor para tareas CPU-bound"""
    print("\n=== 6. ProcessPoolExecutor (CPU-bound) ===")
    inicio = time.time()
    
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(tarea_cpu_intensiva, f"Tarea {i+1}", 1000000)
            for i in range(3)
        ]
        # Espera a que todas completen
        for future in futures:
            future.result()
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s\n")


# ============================================================================
# 7. COMPARACIÓN: Hilos vs Procesos con GIL
# ============================================================================
def trabajo_cpu_pesado(nombre, iteraciones=5000000):
    """Trabajo CPU intensivo para demostrar el efecto del GIL"""
    resultado = 0
    for i in range(iteraciones):
        resultado += i * 2
    print(f"[{nombre}] Completado: {resultado}")


def ejemplo_gil_hilos():
    """Hilos con GIL: no hay paralelismo real para CPU-bound"""
    print("\n=== 7a. HILOS con GIL (CPU-bound) - NO paralelo ===")
    inicio = time.time()
    
    hilos = []
    for i in range(3):
        hilo = threading.Thread(
            target=trabajo_cpu_pesado, 
            args=(f"Hilo {i+1}", 5000000)
        )
        hilos.append(hilo)
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s (GIL limita el paralelismo)\n")


def ejemplo_gil_procesos():
    """Procesos: sí hay paralelismo real para CPU-bound"""
    print("\n=== 7b. PROCESOS (CPU-bound) - SÍ paralelo ===")
    inicio = time.time()
    
    procesos = []
    for i in range(3):
        proceso = multiprocessing.Process(
            target=trabajo_cpu_pesado,
            args=(f"Proceso {i+1}", 5000000)
        )
        procesos.append(proceso)
        proceso.start()
    
    for proceso in procesos:
        proceso.join()
    
    tiempo_total = time.time() - inicio
    print(f"Tiempo total: {tiempo_total:.2f}s (paralelismo real)\n")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================
def main():
    """Ejecuta todos los ejemplos"""
    print("=" * 60)
    print("EJEMPLOS DE MODELOS DE EJECUCIÓN COMPUTACIONAL")
    print("=" * 60)
    print(f"Núcleos disponibles: {os.cpu_count()}")
    print(f"PID del proceso principal: {os.getpid()}")
    
    # Ejemplos básicos
    ejemplo_secuencial()
    ejemplo_hilos()
    
    # Ejemplo asíncrono (requiere event loop)
    print("\n=== 4. ASÍNCRONO (Event Loop) ===")
    inicio = time.time()
    asyncio.run(ejemplo_asincrono())
    
    # Ejemplos con executors
    ejemplo_thread_pool()
    
    # Nota: Los ejemplos de procesos pueden ser más lentos en algunos sistemas
    # Descomenta para probar:
    # ejemplo_procesos()
    # ejemplo_process_pool()
    # ejemplo_gil_hilos()
    # ejemplo_gil_procesos()
    
    print("=" * 60)
    print("Ejemplos completados!")
    print("=" * 60)


if __name__ == "__main__":
    # Importante para multiprocessing en Windows/macOS
    multiprocessing.freeze_support()
    main()

