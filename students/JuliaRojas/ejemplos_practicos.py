"""
Ejemplos prácticos: Hilos vs Procesos y Modelos de Ejecución
Basado en el contenido de computo_distribuido/
"""

import time
import requests
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import threading

# ============================================================================
# 1. HILOS vs PROCESOS: I/O-bound vs CPU-bound
# ============================================================================

def descargar_url(url):
    """Tarea I/O-bound: espera respuesta de red"""
    try:
        response = requests.get(url, timeout=5)
        return f"{url}: {len(response.content)} bytes"
    except:
        return f"{url}: Error"

def calcular_primos(n):
    """Tarea CPU-bound: cálculo intensivo"""
    count = 0
    for num in range(2, n):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            count += 1
    return count

# Ejemplo 1: I/O-bound con ThreadPoolExecutor (recomendado)
def ejemplo_io_bound_hilos():
    print("\n=== I/O-bound con Hilos ===")
    urls = [
        "http://httpbin.org/delay/1",
        "http://httpbin.org/delay/1",
        "http://httpbin.org/delay/1",
    ]
    
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        resultados = list(executor.map(descargar_url, urls))
    tiempo = time.time() - inicio
    
    print(f"Tiempo con hilos: {tiempo:.2f}s")
    print(f"Resultados: {resultados}")

# Ejemplo 2: CPU-bound con ProcessPoolExecutor (recomendado)
def ejemplo_cpu_bound_procesos():
    print("\n=== CPU-bound con Procesos ===")
    numeros = [10000, 10000, 10000]
    
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=3) as executor:
        resultados = list(executor.map(calcular_primos, numeros))
    tiempo = time.time() - inicio
    
    print(f"Tiempo con procesos: {tiempo:.2f}s")
    print(f"Primos encontrados: {resultados}")

# ============================================================================
# 2. MODELOS DE EJECUCIÓN
# ============================================================================

# Modelo 1: SECUENCIAL
def modelo_secuencial():
    """Tareas ejecutan una después de otra"""
    print("\n=== Modelo SECUENCIAL ===")
    inicio = time.time()
    
    # Tarea 1
    time.sleep(0.5)
    print("Tarea 1 completada")
    
    # Tarea 2
    time.sleep(0.5)
    print("Tarea 2 completada")
    
    # Tarea 3
    time.sleep(0.5)
    print("Tarea 3 completada")
    
    tiempo = time.time() - inicio
    print(f"Tiempo total: {tiempo:.2f}s")

# Modelo 2: ASÍNCRONO NO CONCURRENTE
async def tarea_async(nombre, delay):
    """Tarea asíncrona con espera"""
    print(f"{nombre}: Iniciando...")
    await asyncio.sleep(delay)  # Simula I/O
    print(f"{nombre}: Completada")
    return nombre

async def modelo_asincrono_no_concurrente():
    """Event loop pero sin aprovechar waits (secuencial)"""
    print("\n=== Modelo ASÍNCRONO NO CONCURRENTE ===")
    inicio = time.time()
    
    # Ejecuta secuencialmente (no usa gather)
    await tarea_async("Tarea 1", 0.5)
    await tarea_async("Tarea 2", 0.5)
    await tarea_async("Tarea 3", 0.5)
    
    tiempo = time.time() - inicio
    print(f"Tiempo total: {tiempo:.2f}s")

# Modelo 3: CONCURRENTE NO ASÍNCRONO
def tarea_cpu(nombre, iteraciones):
    """Tarea CPU-bound sin waits"""
    resultado = 0
    for i in range(iteraciones):
        resultado += i * i
    print(f"{nombre}: Completada (resultado: {resultado})")
    return resultado

def modelo_concurrente_no_asincrono():
    """Múltiples threads con time-slicing (P=1)"""
    print("\n=== Modelo CONCURRENTE NO ASÍNCRONO ===")
    inicio = time.time()
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=tarea_cpu, args=(f"Tarea {i+1}", 1000000))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    tiempo = time.time() - inicio
    print(f"Tiempo total: {tiempo:.2f}s")

# Modelo 4: CONCURRENTE Y ASÍNCRONO
async def modelo_asincrono_concurrente():
    """Event loop aprovechando waits"""
    print("\n=== Modelo ASÍNCRONO CONCURRENTE ===")
    inicio = time.time()
    
    # Ejecuta concurrentemente (aprovecha waits)
    tareas = [
        tarea_async("Tarea 1", 0.5),
        tarea_async("Tarea 2", 0.5),
        tarea_async("Tarea 3", 0.5),
    ]
    resultados = await asyncio.gather(*tareas)
    
    tiempo = time.time() - inicio
    print(f"Tiempo total: {tiempo:.2f}s (más rápido!)")
    print(f"Resultados: {resultados}")

# Modelo 5: PARALELO
def modelo_paralelo():
    """Múltiples procesos en múltiples cores"""
    print("\n=== Modelo PARALELO ===")
    inicio = time.time()
    
    # CPU-bound en paralelo
    numeros = [5000000, 5000000, 5000000]
    with ProcessPoolExecutor(max_workers=3) as executor:
        resultados = list(executor.map(calcular_primos, numeros))
    
    tiempo = time.time() - inicio
    print(f"Tiempo total: {tiempo:.2f}s")
    print(f"Primos encontrados: {resultados}")

# ============================================================================
# 3. COMPARACIÓN: ThreadPoolExecutor vs ProcessPoolExecutor
# ============================================================================

def comparacion_executors():
    """Demuestra cuándo usar cada executor"""
    print("\n=== COMPARACIÓN: ThreadPool vs ProcessPool ===")
    
    # I/O-bound: ThreadPool es mejor
    print("\n1. I/O-bound (descargas):")
    urls = ["http://httpbin.org/delay/1"] * 3
    
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(descargar_url, urls))
    tiempo_hilos = time.time() - inicio
    print(f"   ThreadPool: {tiempo_hilos:.2f}s")
    
    # CPU-bound: ProcessPool es mejor
    print("\n2. CPU-bound (cálculos):")
    numeros = [100000] * 3
    
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(calcular_primos, numeros))
    tiempo_hilos_cpu = time.time() - inicio
    print(f"   ThreadPool: {tiempo_hilos_cpu:.2f}s (limitado por GIL)")
    
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=3) as executor:
        list(executor.map(calcular_primos, numeros))
    tiempo_procesos = time.time() - inicio
    print(f"   ProcessPool: {tiempo_procesos:.2f}s (paralelismo real)")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EJEMPLOS: HILOS vs PROCESOS y MODELOS DE EJECUCIÓN")
    print("=" * 60)
    
    # Hilos vs Procesos
    ejemplo_io_bound_hilos()
    ejemplo_cpu_bound_procesos()
    
    # Modelos de ejecución
    modelo_secuencial()
    
    # Nota: Los ejemplos async requieren ejecutarse en un event loop
    print("\n=== Para ejecutar modelos asíncronos, usa: ===")
    print("asyncio.run(modelo_asincrono_no_concurrente())")
    print("asyncio.run(modelo_asincrono_concurrente())")
    
    modelo_concurrente_no_asincrono()
    modelo_paralelo()
    
    # Comparación
    comparacion_executors()
    
    print("\n" + "=" * 60)
    print("RESUMEN:")
    print("- I/O-bound → ThreadPoolExecutor")
    print("- CPU-bound → ProcessPoolExecutor")
    print("- Asíncrono concurrente → asyncio.gather()")
    print("- Paralelo → ProcessPoolExecutor con múltiples cores")
    print("=" * 60)

