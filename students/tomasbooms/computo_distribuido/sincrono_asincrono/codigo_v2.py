"""
Ejemplos prácticos: Modelos de Ejecución Computacional
=====================================================

Este archivo demuestra los diferentes modelos de ejecución explicados en:
- README_v4.md (marco matemático)
- README_codigo.md (implementación en Python)

Cada ejemplo muestra un patrón diferente de ejecución.
"""

import time
import os
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime


def tiempo():
    """Retorna timestamp legible: HH:MM:SS.mmm"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# ============================================================================
# 1. SECUENCIAL (Sección 2)
# ============================================================================

def tarea_cpu(nombre, duracion=0.5):
    """Simula trabajo CPU-bound"""
    print(f"[{tiempo()}] {nombre}: Inicio")
    time.sleep(duracion)  # Simula cómputo
    print(f"[{tiempo()}] {nombre}: Fin")
    return f"Resultado de {nombre}"


def ejemplo_secuencial():
    """Ejecución secuencial: una tarea termina antes de que inicie la siguiente"""
    print("\n" + "="*60)
    print("1. EJECUCIÓN SECUENCIAL")
    print("="*60)
    
    resultado1 = tarea_cpu("Tarea A", 0.5)
    resultado2 = tarea_cpu("Tarea B", 0.5)
    resultado3 = tarea_cpu("Tarea C", 0.5)
    
    print(f"Todas completadas. Resultados: {resultado1}, {resultado2}, {resultado3}")


# ============================================================================
# 2. ASÍNCRONO NO CONCURRENTE (Sección 3)
# ============================================================================

async def tarea_async(nombre, duracion=0.5):
    """Simula tarea asíncrona con espera"""
    print(f"[{tiempo()}] {nombre}: Inicio")
    await asyncio.sleep(duracion)  # Espera (wait) - pero no se aprovecha
    print(f"[{tiempo()}] {nombre}: Fin")
    return f"Resultado de {nombre}"


async def ejemplo_asincrono_no_concurrente():
    """Asíncrono pero NO concurrente: tareas se ejecutan una tras otra"""
    print("\n" + "="*60)
    print("2. ASÍNCRONO NO CONCURRENTE")
    print("="*60)
    
    # Ejecución secuencial con await
    resultado1 = await tarea_async("Tarea A", 0.5)
    resultado2 = await tarea_async("Tarea B", 0.5)
    resultado3 = await tarea_async("Tarea C", 0.5)
    
    print(f"Todas completadas. Resultados: {resultado1}, {resultado2}, {resultado3}")


# ============================================================================
# 3. ASÍNCRONO Y CONCURRENTE (Sección 5)
# ============================================================================

async def ejemplo_asincrono_concurrente():
    """Asíncrono Y concurrente: aprovecha los waits para ejecutar otras tareas"""
    print("\n" + "="*60)
    print("3. ASÍNCRONO Y CONCURRENTE (con asyncio.gather)")
    print("="*60)
    
    # Todas las tareas se ejecutan concurrentemente
    resultados = await asyncio.gather(
        tarea_async("Tarea A", 0.5),
        tarea_async("Tarea B", 0.5),
        tarea_async("Tarea C", 0.5)
    )
    
    print(f"Todas completadas. Resultados: {resultados}")


# ============================================================================
# 4. CONCURRENTE NO ASÍNCRONO (Sección 4) - Threading
# ============================================================================

def ejemplo_threading():
    """Concurrencia con threads: time-slicing en un solo core (P=1)"""
    print("\n" + "="*60)
    print("4. CONCURRENTE NO ASÍNCRONO (Threading)")
    print("="*60)
    
    def tarea_thread(nombre, duracion=0.5):
        print(f"[{tiempo()}] {nombre}: Inicio (Thread: {threading.current_thread().name})")
        time.sleep(duracion)  # Simula trabajo CPU-bound
        print(f"[{tiempo()}] {nombre}: Fin")
        return f"Resultado de {nombre}"
    
    # Crear threads
    threads = []
    resultados = {}
    
    def worker(nombre):
        resultados[nombre] = tarea_thread(nombre, 0.5)
    
    for nombre in ["Tarea A", "Tarea B", "Tarea C"]:
        t = threading.Thread(target=worker, args=(nombre,))
        threads.append(t)
        t.start()
    
    # Esperar a que todos terminen
    for t in threads:
        t.join()
    
    print(f"Todas completadas. Resultados: {resultados}")


# ============================================================================
# 5. PARALELO (Sección 6) - ProcessPoolExecutor
# ============================================================================

def tarea_cpu_intensiva(nombre, duracion=0.5):
    """Tarea CPU-bound para procesamiento paralelo"""
    print(f"[{tiempo()}] {nombre}: Inicio (PID: {os.getpid()})")
    # Simula trabajo intensivo
    suma = sum(i**2 for i in range(100000))
    time.sleep(duracion)
    print(f"[{tiempo()}] {nombre}: Fin (suma={suma})")
    return f"Resultado de {nombre}"


def ejemplo_paralelo():
    """Paralelismo real: múltiples procesos en múltiples cores"""
    print("\n" + "="*60)
    print("5. PARALELO (ProcessPoolExecutor)")
    print("="*60)
    
    # Usar ProcessPoolExecutor para trabajo CPU-bound
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(tarea_cpu_intensiva, "Tarea A", 0.5),
            executor.submit(tarea_cpu_intensiva, "Tarea B", 0.5),
            executor.submit(tarea_cpu_intensiva, "Tarea C", 0.5)
        ]
        
        resultados = [f.result() for f in futures]
    
    print(f"Todas completadas. Resultados: {resultados}")


# ============================================================================
# 6. COMPARACIÓN: ThreadPoolExecutor vs ProcessPoolExecutor
# ============================================================================

def ejemplo_comparacion_executors():
    """Compara ThreadPoolExecutor (I/O-bound) vs ProcessPoolExecutor (CPU-bound)"""
    print("\n" + "="*60)
    print("6. COMPARACIÓN: Threads vs Procesos")
    print("="*60)
    
    def tarea_io(nombre):
        """Simula I/O (descarga, lectura de archivo, etc.)"""
        print(f"[{tiempo()}] {nombre}: Inicio I/O")
        time.sleep(0.5)  # Simula espera de red/disco
        print(f"[{tiempo()}] {nombre}: Fin I/O")
        return f"Resultado I/O de {nombre}"
    
    def tarea_cpu(nombre):
        """Simula trabajo CPU intensivo"""
        print(f"[{tiempo()}] {nombre}: Inicio CPU")
        suma = sum(i**2 for i in range(500000))  # Cómputo pesado
        print(f"[{tiempo()}] {nombre}: Fin CPU (suma={suma})")
        return f"Resultado CPU de {nombre}"
    
    print("\n--- ThreadPoolExecutor (I/O-bound) ---")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(tarea_io, f"Tarea {i}") for i in range(3)]
        resultados_threads = [f.result() for f in futures]
    
    print("\n--- ProcessPoolExecutor (CPU-bound) ---")
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(tarea_cpu, f"Tarea {i}") for i in range(3)]
        resultados_procesos = [f.result() for f in futures]
    
    print(f"\nThreads: {resultados_threads}")
    print(f"Procesos: {resultados_procesos}")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "="*60)
    print("EJEMPLOS DE MODELOS DE EJECUCIÓN COMPUTACIONAL")
    print("="*60)
    
    # 1. Secuencial
    ejemplo_secuencial()
    
    # 2. Asíncrono no concurrente
    print("\nEjecutando ejemplo asíncrono no concurrente...")
    asyncio.run(ejemplo_asincrono_no_concurrente())
    
    # 3. Asíncrono concurrente
    print("\nEjecutando ejemplo asíncrono concurrente...")
    asyncio.run(ejemplo_asincrono_concurrente())
    
    # 4. Threading (concurrente no asíncrono)
    ejemplo_threading()
    
    # 5. Paralelo (multiprocessing)
    try:
        import os
        ejemplo_paralelo()
    except Exception as e:
        print(f"Error en ejemplo paralelo: {e}")
        print("(Puede requerir configuración especial en algunos sistemas)")
    
    # 6. Comparación
    ejemplo_comparacion_executors()
    
    print("\n" + "="*60)
    print("FIN DE EJEMPLOS")
    print("="*60)


if __name__ == "__main__":
    main()

