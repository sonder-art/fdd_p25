"""
Ejemplos simples y breves para entender hilos, procesos y modelos de ejecución
"""

import time
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio

# ============================================================================
# EJEMPLO 1: I/O-bound con Hilos (ThreadPoolExecutor)
# ============================================================================

def simular_descarga(url_id):
    """Simula descarga (I/O-bound)"""
    time.sleep(1)  # Simula espera de red
    return f"Descarga {url_id} completada"

def ejemplo_hilos_io():
    print("1. I/O-bound con HILOS:")
    inicio = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        resultados = list(executor.map(simular_descarga, [1, 2, 3]))
    
    print(f"   Tiempo: {time.time() - inicio:.2f}s (3 tareas en ~1s)")
    print(f"   {resultados}\n")

# ============================================================================
# EJEMPLO 2: CPU-bound con Procesos (ProcessPoolExecutor)
# ============================================================================

def calcular_factorial(n):
    """Cálculo intensivo (CPU-bound)"""
    resultado = 0
    for i in range(1, n + 1):
        resultado += sum(range(i))  # Suma acumulativa
    return resultado

def ejemplo_procesos_cpu():
    print("2. CPU-bound con PROCESOS:")
    inicio = time.time()
    
    with ProcessPoolExecutor(max_workers=3) as executor:
        resultados = list(executor.map(calcular_factorial, [10000, 10000, 10000]))
    
    print(f"   Tiempo: {time.time() - inicio:.2f}s")
    print(f"   Resultados: {resultados}\n")

# ============================================================================
# EJEMPLO 3: Secuencial (sin paralelismo)
# ============================================================================

def ejemplo_secuencial():
    print("3. SECUENCIAL (sin paralelismo):")
    inicio = time.time()
    
    for i in [1, 2, 3]:
        time.sleep(0.5)
        print(f"   Tarea {i} completada")
    
    print(f"   Tiempo: {time.time() - inicio:.2f}s (3 × 0.5s = 1.5s)\n")

# ============================================================================
# EJEMPLO 4: Asíncrono Concurrente (asyncio)
# ============================================================================

async def tarea_async(nombre, delay):
    await asyncio.sleep(delay)
    return f"{nombre} completada"

async def ejemplo_asincrono():
    print("4. ASÍNCRONO CONCURRENTE (asyncio):")
    inicio = time.time()
    
    # Ejecuta 3 tareas concurrentemente
    resultados = await asyncio.gather(
        tarea_async("Tarea 1", 0.5),
        tarea_async("Tarea 2", 0.5),
        tarea_async("Tarea 3", 0.5)
    )
    
    print(f"   Tiempo: {time.time() - inicio:.2f}s (~0.5s, no 1.5s!)")
    print(f"   {resultados}\n")

# ============================================================================
# EJEMPLO 5: Comparación directa
# ============================================================================

def comparacion_rapida():
    print("5. COMPARACIÓN RÁPIDA:")
    
    # Secuencial
    inicio = time.time()
    for i in range(3):
        time.sleep(0.3)
    secuencial = time.time() - inicio
    
    # Con hilos (I/O-bound)
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(lambda x: time.sleep(0.3), range(3)))
    hilos = time.time() - inicio
    
    print(f"   Secuencial: {secuencial:.2f}s")
    print(f"   Con hilos:  {hilos:.2f}s")
    print(f"   Mejora: {secuencial/hilos:.1f}x más rápido\n")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EJEMPLOS SIMPLES: HILOS, PROCESOS Y MODELOS DE EJECUCIÓN")
    print("=" * 60)
    print()
    
    # Ejemplos síncronos
    ejemplo_hilos_io()
    ejemplo_procesos_cpu()
    ejemplo_secuencial()
    comparacion_rapida()
    
    # Ejemplo asíncrono
    print("Ejecutando ejemplo asíncrono...")
    asyncio.run(ejemplo_asincrono())
    
    print("=" * 60)
    print("RESUMEN:")
    print("  • I/O-bound (red, disco) → ThreadPoolExecutor")
    print("  • CPU-bound (cálculos)   → ProcessPoolExecutor")
    print("  • Asíncrono I/O          → asyncio.gather()")
    print("=" * 60)

