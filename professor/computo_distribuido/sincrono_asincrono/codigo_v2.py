import threading
import time
import os
from datetime import datetime

def tiempo():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def tarea_cpu_intensiva(nombre):
    """Trabajo CPU-bound: cálculos sin I/O"""
    print(f"[{tiempo()}] {nombre} - inicio")
    resultado = sum(range(20_000_000))  # Cálculo puro, sin sleep
    print(f"[{tiempo()}] {nombre} - fin (resultado: {resultado})")

print(f"Cores disponibles: {os.cpu_count()}")

# PRUEBA 1: Con threading (GIL limita a 1 core efectivo)
print(f"\n=== CON THREADING (múltiples hilos, 1 core efectivo) ===")
inicio = time.time()
hilo_a = threading.Thread(target=tarea_cpu_intensiva, args=("Thread-A",))
hilo_b = threading.Thread(target=tarea_cpu_intensiva, args=("Thread-B",))
hilo_a.start()
hilo_b.start()
hilo_a.join()
hilo_b.join()
tiempo_threading = time.time() - inicio
print(f"Tiempo total: {tiempo_threading:.2f}s")

# PRUEBA 2: Con multiprocessing (usa múltiples cores reales)
from multiprocessing import Process

def tarea_cpu_process(nombre):
    print(f"[{tiempo()}] {nombre} - inicio (PID: {os.getpid()})")
    resultado = sum(range(20_000_000))
    print(f"[{tiempo()}] {nombre} - fin (resultado: {resultado})")

if __name__ == "__main__":
    print(f"\n=== CON MULTIPROCESSING (múltiples procesos, múltiples cores) ===")
    inicio = time.time()
    proc_a = Process(target=tarea_cpu_process, args=("Process-A",))
    proc_b = Process(target=tarea_cpu_process, args=("Process-B",))
    proc_a.start()
    proc_b.start()
    proc_a.join()
    proc_b.join()
    tiempo_multiproc = time.time() - inicio
    print(f"Tiempo total: {tiempo_multiproc:.2f}s")
    
    print(f"\n=== COMPARACIÓN ===")
    print(f"Threading (1 core efectivo por GIL): {tiempo_threading:.2f}s")
    print(f"Multiprocessing (2+ cores reales): {tiempo_multiproc:.2f}s")
    print(f"Speedup con multiprocessing: {tiempo_threading/tiempo_multiproc:.2f}x")

# Salida típica en máquina con 8 cores:
# Cores disponibles: 8