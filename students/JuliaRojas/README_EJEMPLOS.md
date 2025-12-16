# Ejemplos Prácticos: Hilos, Procesos y Modelos de Ejecución

Este directorio contiene ejemplos de código para entender los conceptos de computación distribuida, hilos, procesos y diferentes modelos de ejecución.

## Archivos

- `ejemplos_simples.py` - Ejemplos breves y fáciles de entender
- `ejemplos_practicos.py` - Ejemplos más completos con casos reales

## Requisitos

```bash
pip install requests  # Solo para ejemplos con descargas HTTP
```

## Ejecución Rápida

### Ejemplos Simples (recomendado para empezar)

```bash
python ejemplos_simples.py
```

Este archivo demuestra:
1. **I/O-bound con hilos** - Descargas simuladas
2. **CPU-bound con procesos** - Cálculos intensivos
3. **Ejecución secuencial** - Sin paralelismo
4. **Asíncrono concurrente** - Con asyncio
5. **Comparación directa** - Secuencial vs paralelo

### Ejemplos Prácticos (más detallados)

```bash
python ejemplos_practicos.py
```

## Conceptos Clave

### 1. Hilos vs Procesos

**ThreadPoolExecutor** (hilos):
- ✅ Ideal para **I/O-bound** (red, disco, bases de datos)
- ✅ Bajo overhead
- ✅ Comparten memoria
- ❌ Limitado por GIL en Python para CPU-bound

**ProcessPoolExecutor** (procesos):
- ✅ Ideal para **CPU-bound** (cálculos, procesamiento)
- ✅ Paralelismo real (evita GIL)
- ✅ Aislamiento de memoria
- ❌ Mayor overhead de creación

### 2. Modelos de Ejecución

1. **Secuencial**: Tareas una después de otra
2. **Asíncrono no concurrente**: Hay esperas pero no se aprovechan
3. **Concurrente no asíncrono**: Time-slicing sin waits
4. **Asíncrono concurrente**: Aprovecha esperas (asyncio)
5. **Paralelo**: Múltiples cores trabajando simultáneamente

## Ejemplos de Uso

### Ejemplo 1: Descargar múltiples URLs (I/O-bound)

```python
from concurrent.futures import ThreadPoolExecutor

urls = ["http://example.com"] * 10

with ThreadPoolExecutor(max_workers=5) as executor:
    resultados = list(executor.map(descargar_url, urls))
```

### Ejemplo 2: Procesar imágenes (CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor

imagenes = ["img1.jpg", "img2.jpg", "img3.jpg"]

with ProcessPoolExecutor(max_workers=4) as executor:
    resultados = list(executor.map(procesar_imagen, imagenes))
```

### Ejemplo 3: Múltiples tareas asíncronas

```python
import asyncio

async def main():
    resultados = await asyncio.gather(
        tarea_1(),
        tarea_2(),
        tarea_3()
    )
    return resultados

asyncio.run(main())
```

## Decisión Rápida

```
¿Tu tarea espera mucho tiempo (red, disco)?
├─ Sí → ThreadPoolExecutor o asyncio
└─ No → ¿Es cálculo intensivo?
    ├─ Sí → ProcessPoolExecutor
    └─ No → Ejecución secuencial está bien
```

## Referencias

- Ver `hilos_procesos/README.md` para explicación detallada de hilos vs procesos
- Ver `sincrono_asincrono/README_v4.md` para framework matemático completo

