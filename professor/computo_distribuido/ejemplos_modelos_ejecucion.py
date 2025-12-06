#!/usr/bin/env python3
"""
Ejemplos de Modelos de Ejecución Computacional
Basado en los materiales de professor/computo_distribuido/

Este archivo demuestra los 5 modelos principales con la analogía de la cocina.
"""

import asyncio
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime


def timestamp():
    """Retorna timestamp legible HH:MM:SS.mmm"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# =============================================================================
# MODELO 1: SECUENCIAL
# =============================================================================
def modelo_1_secuencial():
    """
    Un chef hace una orden completa antes de iniciar la siguiente.
    No hay concurrencia ni aprovechamiento de esperas.
    """
    print(f"\n{'='*70}")
    print("MODELO 1: SECUENCIAL")
    print(f"{'='*70}")
    
    def preparar_cafe():
        print(f"[{timestamp()}] ☕ Café: moler granos...")
        time.sleep(1)
        print(f"[{timestamp()}] ☕ Café: hervir agua...")
        time.sleep(1)
        print(f"[{timestamp()}] ☕ Café: LISTO")
    
    def tostar_pan():
        print(f"[{timestamp()}] 🍞 Pan: meter en tostadora...")
        time.sleep(0.5)
        print(f"[{timestamp()}] 🍞 Pan: LISTO")
    
    inicio = time.time()
    preparar_cafe()  # Espera a que termine
    tostar_pan()     # Solo entonces inicia
    tiempo_total = time.time() - inicio
    
    print(f"⏱️  Tiempo total: {tiempo_total:.2f}s (suma de todas las tareas)")


# =============================================================================
# MODELO 2: ASÍNCRONO pero NO CONCURRENTE
# =============================================================================
async def modelo_2_async_no_concurrente():
    """
    El chef puede esperar (await), pero no inicia otra orden mientras espera.
    CPU ociosa durante las esperas.
    """
    print(f"\n{'='*70}")
    print("MODELO 2: ASÍNCRONO pero NO CONCURRENTE")
    print(f"{'='*70}")
    
    async def preparar_cafe():
        print(f"[{timestamp()}] ☕ Café: inicio cafetera...")
        await asyncio.sleep(1)  # Espera (wait)
        print(f"[{timestamp()}] ☕ Café: LISTO")
    
    async def tostar_pan():
        print(f"[{timestamp()}] 🍞 Pan: inicio tostadora...")
        await asyncio.sleep(0.5)  # Espera (wait)
        print(f"[{timestamp()}] 🍞 Pan: LISTO")
    
    inicio = time.time()
    await preparar_cafe()  # Espera a que termine (no aprovecha el wait)
    await tostar_pan()     # Solo entonces inicia
    tiempo_total = time.time() - inicio
    
    print(f"⏱️  Tiempo total: {tiempo_total:.2f}s (CPU ociosa durante waits)")


# =============================================================================
# MODELO 3: CONCURRENTE pero NO ASÍNCRONO
# =============================================================================
def modelo_3_concurrente_no_async():
    """
    Tres tareas CPU-bound que se alternan por time-slicing.
    No hay esperas reales, solo cambios de contexto.
    """
    print(f"\n{'='*70}")
    print("MODELO 3: CONCURRENTE pero NO ASÍNCRONO (time-slicing)")
    print(f"{'='*70}")
    
    def tarea_cpu_intensiva(nombre, iteraciones):
        print(f"[{timestamp()}] {nombre}: INICIO")
        resultado = sum(range(iteraciones))
        print(f"[{timestamp()}] {nombre}: FIN (resultado={resultado})")
    
    inicio = time.time()
    
    # Crear 3 hilos (se alternan en CPU por time-slicing)
    hilos = [
        threading.Thread(target=tarea_cpu_intensiva, args=("🥘 Risotto", 5_000_000)),
        threading.Thread(target=tarea_cpu_intensiva, args=("🍲 Salsa", 5_000_000)),
        threading.Thread(target=tarea_cpu_intensiva, args=("🥗 Vegetales", 5_000_000)),
    ]
    
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    
    tiempo_total = time.time() - inicio
    print(f"⏱️  Tiempo total: {tiempo_total:.2f}s (alternancia, sin paralelismo por GIL)")


# =============================================================================
# MODELO 4: ASÍNCRONO Y CONCURRENTE (sin paralelismo)
# =============================================================================
async def modelo_4_async_concurrente():
    """
    El chef inicia cafetera Y tostadora casi simultáneamente.
    Mientras ambas esperan, puede hacer otras cosas.
    Aprovecha los waits para ejecutar otras tareas.
    """
    print(f"\n{'='*70}")
    print("MODELO 4: ASÍNCRONO Y CONCURRENTE (event loop)")
    print(f"{'='*70}")
    
    async def preparar_cafe():
        print(f"[{timestamp()}] ☕ Café: inicio cafetera...")
        await asyncio.sleep(1)  # Espera (wait) - libera CPU
        print(f"[{timestamp()}] ☕ Café: LISTO")
        return "café"
    
    async def tostar_pan():
        print(f"[{timestamp()}] 🍞 Pan: inicio tostadora...")
        await asyncio.sleep(0.5)  # Espera (wait) - libera CPU
        print(f"[{timestamp()}] 🍞 Pan: LISTO")
        return "pan"
    
    async def cortar_fruta():
        print(f"[{timestamp()}] 🍎 Fruta: cortando...")
        await asyncio.sleep(0.3)  # Trabajo
        print(f"[{timestamp()}] 🍎 Fruta: LISTO")
        return "fruta"
    
    inicio = time.time()
    # gather() ejecuta todas concurrentemente, aprovechando waits
    resultados = await asyncio.gather(preparar_cafe(), tostar_pan(), cortar_fruta())
    tiempo_total = time.time() - inicio
    
    print(f"✅ Resultados: {resultados}")
    print(f"⏱️  Tiempo total: {tiempo_total:.2f}s (máximo de las tareas, NO la suma)")


# =============================================================================
# MODELO 5: PARALELO (múltiples cores)
# =============================================================================
def procesar_ingrediente(nombre, complejidad):
    """Función auxiliar para procesamiento paralelo (debe estar a nivel módulo)"""
    pid = os.getpid()
    print(f"[{timestamp()}] {nombre}: INICIO (PID {pid})")
    resultado = sum(range(complejidad))  # CPU-bound
    print(f"[{timestamp()}] {nombre}: FIN (PID {pid}, resultado={resultado})")
    return resultado


def modelo_5_paralelo():
    """
    Múltiples chefs (cores) trabajan simultáneamente.
    Paralelismo real en múltiples CPUs.
    """
    print(f"\n{'='*70}")
    print(f"MODELO 5: PARALELO (múltiples cores)")
    print(f"{'='*70}")
    print(f"Sistema: {os.cpu_count()} cores disponibles")
    
    tareas = [
        ("🥔 Papas", 8_000_000),
        ("🥕 Zanahorias", 6_000_000),
        ("🧅 Cebollas", 5_000_000),
    ]
    
    # Comparación: Secuencial vs Paralelo
    print("\n--- SECUENCIAL (baseline) ---")
    inicio = time.time()
    for nombre, complejidad in tareas:
        procesar_ingrediente(nombre, complejidad)
    tiempo_seq = time.time() - inicio
    print(f"⏱️  Secuencial: {tiempo_seq:.2f}s")
    
    print("\n--- PARALELO (múltiples procesos) ---")
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=3) as executor:
        resultados = list(executor.map(
            procesar_ingrediente, 
            [t[0] for t in tareas],
            [t[1] for t in tareas]
        ))
    tiempo_par = time.time() - inicio
    print(f"⏱️  Paralelo: {tiempo_par:.2f}s")
    print(f"⚡ Speedup: {tiempo_seq/tiempo_par:.2f}x")


# =============================================================================
# DEMOSTRACIÓN: Threading vs Multiprocessing para CPU-bound
# =============================================================================
def tarea_cpu(n):
    """Función auxiliar para demo GIL (debe estar a nivel módulo)"""
    return sum(range(n))


def demo_gil():
    """
    Demuestra el impacto del GIL en tareas CPU-bound.
    Threading NO da paralelismo, Multiprocessing SÍ.
    """
    print(f"\n{'='*70}")
    print("DEMOSTRACIÓN: Impacto del GIL en CPU-bound")
    print(f"{'='*70}")
    
    datos = [10_000_000, 10_000_000]
    
    # ThreadPoolExecutor (limitado por GIL)
    print("--- Threading (limitado por GIL) ---")
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(tarea_cpu, datos))
    tiempo_threading = time.time() - inicio
    print(f"⏱️  Threading: {tiempo_threading:.2f}s (casi secuencial)")
    
    # ProcessPoolExecutor (sin GIL)
    print("\n--- Multiprocessing (sin GIL) ---")
    inicio = time.time()
    with ProcessPoolExecutor(max_workers=2) as executor:
        list(executor.map(tarea_cpu, datos))
    tiempo_multiproc = time.time() - inicio
    print(f"⏱️  Multiprocessing: {tiempo_multiproc:.2f}s (paralelismo real)")
    print(f"⚡ Speedup: {tiempo_threading/tiempo_multiproc:.2f}x")


# =============================================================================
# MAIN: Ejecutar todos los ejemplos
# =============================================================================
def main():
    print("\n" + "="*70)
    print("EJEMPLOS DE MODELOS DE EJECUCIÓN COMPUTACIONAL")
    print("Basado en: professor/computo_distribuido/")
    print("="*70)
    
    # Modelo 1: Secuencial
    modelo_1_secuencial()
    
    # Modelo 2: Async no concurrente
    asyncio.run(modelo_2_async_no_concurrente())
    
    # Modelo 3: Concurrente no async
    modelo_3_concurrente_no_async()
    
    # Modelo 4: Async concurrente
    asyncio.run(modelo_4_async_concurrente())
    
    # Modelo 5: Paralelo
    modelo_5_paralelo()
    
    # Demo GIL
    demo_gil()
    
    print("\n" + "="*70)
    print("RESUMEN DE DECISIONES:")
    print("="*70)
    print("✅ I/O-bound + librerías async  → asyncio (Modelo 4)")
    print("✅ I/O-bound + librerías sync   → ThreadPoolExecutor")
    print("✅ CPU-bound                    → ProcessPoolExecutor (Modelo 5)")
    print("✅ Tarea simple                 → Secuencial (Modelo 1)")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

