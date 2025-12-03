"""
Ejemplos de Computación Distribuida, Concurrencia y Paralelismo
Basado en los conceptos de hilos, procesos, síncrono/asíncrono

Este script contiene ejemplos prácticos de:
1. Hilos vs Procesos (ThreadPoolExecutor vs ProcessPoolExecutor)
2. Ejecución Síncrona vs Asíncrona
3. Concurrencia y Paralelismo
4. I/O-bound vs CPU-bound
"""

import time
import asyncio
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime


# ============================================================================
# UTILIDADES
# ============================================================================

def tiempo():
    """Retorna timestamp legible: HH:MM:SS.mmm"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def print_separador(titulo=""):
    """Imprime un separador visual"""
    print("\n" + "=" * 70)
    if titulo:
        print(f"  {titulo}")
        print("=" * 70)


# ============================================================================
# EJEMPLO 1: HILOS vs PROCESOS - I/O-bound
# ============================================================================

def descargar_url(url_id):
    """
    Simula descarga de URL (I/O-bound).
    Ideal para ThreadPoolExecutor porque pasa mucho tiempo esperando.
    """
    print(f"[{tiempo()}] Iniciando descarga {url_id}")
    time.sleep(1)  # Simula espera de red
    print(f"[{tiempo()}] Completada descarga {url_id}")
    return f"Contenido de {url_id}"


def ejemplo_hilos_io_bound():
    """Ejemplo usando ThreadPoolExecutor para tareas I/O-bound"""
    print_separador("EJEMPLO 1: Hilos para I/O-bound (ThreadPoolExecutor)")
    
    urls = [1, 2, 3, 4]
    
    print("Usando ThreadPoolExecutor (hilos):")
    inicio = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        resultados = list(executor.map(descargar_url, urls))
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")
    print(f"Resultados: {resultados}")


# ============================================================================
# EJEMPLO 2: HILOS vs PROCESOS - CPU-bound
# ============================================================================

def calcular_factorial(n):
    """
    Calcula factorial (CPU-bound).
    Ideal para ProcessPoolExecutor porque requiere cómputo intensivo.
    """
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado


def ejemplo_procesos_cpu_bound():
    """Ejemplo usando ProcessPoolExecutor para tareas CPU-bound"""
    print_separador("EJEMPLO 2: Procesos para CPU-bound (ProcessPoolExecutor)")
    
    numeros = [1000, 1001, 1002, 1003]
    
    print("Usando ProcessPoolExecutor (procesos):")
    inicio = time.time()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        resultados = list(executor.map(calcular_factorial, numeros))
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")
    print(f"Factoriales calculados: {len(resultados)} valores")


# ============================================================================
# EJEMPLO 3: EJECUCIÓN SÍNCRONA (Secuencial)
# ============================================================================

def tarea_sincrona(id_tarea):
    """Tarea que simula trabajo con espera"""
    print(f"[{tiempo()}] Tarea {id_tarea} iniciada")
    time.sleep(1)  # Espera bloqueante
    print(f"[{tiempo()}] Tarea {id_tarea} completada")
    return f"Resultado {id_tarea}"


def ejemplo_sincrono():
    """Ejecución secuencial: una tarea después de otra"""
    print_separador("EJEMPLO 3: Ejecución Síncrona (Secuencial)")
    
    inicio = time.time()
    
    # Ejecuta tareas una después de otra
    resultado1 = tarea_sincrona(1)
    resultado2 = tarea_sincrona(2)
    resultado3 = tarea_sincrona(3)
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")
    print(f"Resultados: {[resultado1, resultado2, resultado3]}")


# ============================================================================
# EJEMPLO 4: EJECUCIÓN ASÍNCRONA (Concurrente)
# ============================================================================

async def tarea_asincrona(id_tarea):
    """Tarea asíncrona que puede pausarse"""
    print(f"[{tiempo()}] Tarea {id_tarea} iniciada")
    await asyncio.sleep(1)  # Espera no bloqueante
    print(f"[{tiempo()}] Tarea {id_tarea} completada")
    return f"Resultado {id_tarea}"


async def ejemplo_asincrono():
    """Ejecución asíncrona concurrente: aprovecha tiempos de espera"""
    print_separador("EJEMPLO 4: Ejecución Asíncrona (Concurrente)")
    
    inicio = time.time()
    
    # Ejecuta tareas concurrentemente usando asyncio.gather
    resultados = await asyncio.gather(
        tarea_asincrona(1),
        tarea_asincrona(2),
        tarea_asincrona(3)
    )
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")
    print(f"Resultados: {resultados}")


# ============================================================================
# EJEMPLO 5: ASÍNCRONO NO CONCURRENTE
# ============================================================================

async def ejemplo_asincrono_no_concurrente():
    """
    Ejecución asíncrona pero NO concurrente.
    Las tareas se ejecutan secuencialmente aunque usen await.
    """
    print_separador("EJEMPLO 5: Asíncrono NO Concurrente")
    
    inicio = time.time()
    
    # Ejecuta tareas secuencialmente (una después de otra)
    resultado1 = await tarea_asincrona(1)
    resultado2 = await tarea_asincrona(2)
    resultado3 = await tarea_asincrona(3)
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")
    print(f"Resultados: {[resultado1, resultado2, resultado3]}")


# ============================================================================
# EJEMPLO 6: CONCURRENTE NO ASÍNCRONO (Threading con CPU-bound)
# ============================================================================

def tarea_cpu_intensiva(id_tarea, iteraciones=1000000):
    """Tarea CPU-bound que no tiene esperas reales"""
    print(f"[{tiempo()}] Tarea {id_tarea} iniciada")
    suma = 0
    for i in range(iteraciones):
        suma += i
    print(f"[{tiempo()}] Tarea {id_tarea} completada (suma={suma})")
    return suma


def ejemplo_concurrente_no_asincrono():
    """Concurrencia con threading pero sin asincronía (time-slicing)"""
    print_separador("EJEMPLO 6: Concurrente NO Asíncrono (Threading)")
    
    inicio = time.time()
    
    # Crea múltiples hilos que compiten por CPU
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=tarea_cpu_intensiva, args=(i+1, 500000))
        hilos.append(hilo)
        hilo.start()
    
    # Espera a que todos terminen
    for hilo in hilos:
        hilo.join()
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")


# ============================================================================
# EJEMPLO 7: COMPARACIÓN DIRECTA: Hilos vs Procesos
# ============================================================================

def trabajo_cpu(n):
    """Trabajo CPU-bound para comparar"""
    resultado = 0
    for i in range(n):
        resultado += i ** 2
    return resultado


def ejemplo_comparacion_hilos_procesos():
    """Compara ThreadPoolExecutor vs ProcessPoolExecutor en CPU-bound"""
    print_separador("EJEMPLO 7: Comparación Hilos vs Procesos (CPU-bound)")
    
    tareas = [1000000, 1000000, 1000000, 1000000]
    
    # Con hilos (limitado por GIL en Python)
    print("\n--- Usando ThreadPoolExecutor (hilos) ---")
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        resultados_hilos = list(executor.map(trabajo_cpu, tareas))
    tiempo_hilos = time.time() - inicio
    print(f"Tiempo con hilos: {tiempo_hilos:.2f} segundos")
    
    # Con procesos (evita GIL)
    print("\n--- Usando ProcessPoolExecutor (procesos) ---")
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        resultados_procesos = list(executor.map(trabajo_cpu, tareas))
    tiempo_procesos = time.time() - inicio
    print(f"Tiempo con procesos: {tiempo_procesos:.2f} segundos")
    
    print(f"\nSpeedup: {tiempo_hilos/tiempo_procesos:.2f}x más rápido con procesos")


# ============================================================================
# EJEMPLO 8: ASÍNCRONO CONCURRENTE (Event Loop)
# ============================================================================

async def descargar_asincrono(url_id):
    """Simula descarga asíncrona"""
    print(f"[{tiempo()}] Descarga {url_id} iniciada")
    await asyncio.sleep(1)  # Simula espera de red
    print(f"[{tiempo()}] Descarga {url_id} completada")
    return f"Datos de {url_id}"


async def ejemplo_asincrono_concurrente():
    """Event loop con múltiples tareas concurrentes"""
    print_separador("EJEMPLO 8: Asíncrono Concurrente (Event Loop)")
    
    inicio = time.time()
    
    # Crea múltiples tareas y las ejecuta concurrentemente
    tareas = [descargar_asincrono(i) for i in range(1, 6)]
    resultados = await asyncio.gather(*tareas)
    
    tiempo_total = time.time() - inicio
    print(f"\nTiempo total: {tiempo_total:.2f} segundos")
    print(f"Resultados: {resultados}")


# ============================================================================
# EJEMPLO 9: SINCRONIZACIÓN CON LOCKS (Threading)
# ============================================================================

contador_compartido = 0
lock = threading.Lock()


def incrementar_con_lock():
    """Incrementa contador compartido de forma segura"""
    global contador_compartido
    for _ in range(100000):
        with lock:  # Adquiere el lock, incrementa, libera el lock
            contador_compartido += 1


def incrementar_sin_lock():
    """Incrementa contador compartido SIN protección (race condition)"""
    global contador_compartido
    for _ in range(100000):
        contador_compartido += 1  # ⚠️ Race condition potencial


def ejemplo_sincronizacion():
    """Demuestra la necesidad de locks en threading"""
    print_separador("EJEMPLO 9: Sincronización con Locks")
    
    global contador_compartido
    
    # Sin lock (puede tener race conditions)
    print("\n--- Sin lock (puede tener problemas) ---")
    contador_compartido = 0
    hilos = [threading.Thread(target=incrementar_sin_lock) for _ in range(3)]
    inicio = time.time()
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    tiempo_sin_lock = time.time() - inicio
    print(f"Valor final: {contador_compartido} (esperado: 300000)")
    print(f"Tiempo: {tiempo_sin_lock:.2f} segundos")
    
    # Con lock (seguro)
    print("\n--- Con lock (seguro) ---")
    contador_compartido = 0
    hilos = [threading.Thread(target=incrementar_con_lock) for _ in range(3)]
    inicio = time.time()
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    tiempo_con_lock = time.time() - inicio
    print(f"Valor final: {contador_compartido} (esperado: 300000)")
    print(f"Tiempo: {tiempo_con_lock:.2f} segundos")


# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================

def menu():
    """Menú interactivo para ejecutar ejemplos"""
    ejemplos = {
        "1": ("Hilos para I/O-bound", ejemplo_hilos_io_bound),
        "2": ("Procesos para CPU-bound", ejemplo_procesos_cpu_bound),
        "3": ("Ejecución Síncrona (Secuencial)", ejemplo_sincrono),
        "4": ("Ejecución Asíncrona (Concurrente)", lambda: asyncio.run(ejemplo_asincrono())),
        "5": ("Asíncrono NO Concurrente", lambda: asyncio.run(ejemplo_asincrono_no_concurrente())),
        "6": ("Concurrente NO Asíncrono (Threading)", ejemplo_concurrente_no_asincrono),
        "7": ("Comparación Hilos vs Procesos", ejemplo_comparacion_hilos_procesos),
        "8": ("Asíncrono Concurrente (Event Loop)", lambda: asyncio.run(ejemplo_asincrono_concurrente())),
        "9": ("Sincronización con Locks", ejemplo_sincronizacion),
        "0": ("Ejecutar todos", None),
    }
    
    print("\n" + "=" * 70)
    print("  EJEMPLOS DE COMPUTACIÓN DISTRIBUIDA")
    print("=" * 70)
    print("\nSelecciona un ejemplo:")
    for key, (desc, _) in ejemplos.items():
        print(f"  {key}. {desc}")
    print("  q. Salir")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == "q":
        return False
    
    if opcion == "0":
        # Ejecutar todos los ejemplos
        print("\n" + "=" * 70)
        print("  EJECUTANDO TODOS LOS EJEMPLOS")
        print("=" * 70)
        
        ejemplo_hilos_io_bound()
        ejemplo_procesos_cpu_bound()
        ejemplo_sincrono()
        asyncio.run(ejemplo_asincrono())
        asyncio.run(ejemplo_asincrono_no_concurrente())
        ejemplo_concurrente_no_asincrono()
        ejemplo_comparacion_hilos_procesos()
        asyncio.run(ejemplo_asincrono_concurrente())
        ejemplo_sincronizacion()
        
        return True
    
    if opcion in ejemplos:
        _, funcion = ejemplos[opcion]
        if funcion:
            try:
                funcion()
            except Exception as e:
                print(f"\n❌ Error: {e}")
        return True
    
    print("❌ Opción no válida")
    return True


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    # En Windows/macOS, multiprocessing requiere esta protección
    multiprocessing.freeze_support()
    
    print("\n" + "=" * 70)
    print("  EJEMPLOS DE COMPUTACIÓN DISTRIBUIDA")
    print("  Hilos, Procesos, Síncrono, Asíncrono, Concurrencia, Paralelismo")
    print("=" * 70)
    
    # Ejecutar menú interactivo
    continuar = True
    while continuar:
        continuar = menu()
        if continuar:
            input("\nPresiona Enter para continuar...")



