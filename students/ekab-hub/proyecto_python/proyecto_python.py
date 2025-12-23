import numpy as np
import timeit
import math
import json
import platform
from datetime import datetime

# Problema 1

def p1_for(a: np.ndarray, c: float):
    resultado = []
    for x in a:
        resultado.append(x*c)
    return resultado

def p1_comp(a: np.ndarray, c: float):
    return [x * c for x in a]

def p1_gen(a: np.ndarray, c: float):
    for x in a:
        yield x * c

def p1_np(a: np.ndarray, c: float):
    return a * c

def tiempo_p1(n=100_000, num = 5):
    a = np.arange(n, dtype=float)
    c = 2.0
    return (
        timeit.timeit(lambda: p1_for(a, c), number=num),
        timeit.timeit(lambda: p1_comp(a, c), number=num),
        timeit.timeit(lambda: p1_gen(a, c), number=num),
        timeit.timeit(lambda: p1_np(a, c), number=num),
    )

# Problema 2
def p2_for(a: np.ndarray, k: int = 3):
    assert k % 2 == 1
    n = len(a)
    mitad = k//2
    resultado = []
    for i in range(mitad, n-mitad):
        ventana = a[i - mitad: i + mitad + 1]
        resultado.append(float(np.sum(ventana)))
    return resultado

def p2_comp(a: np.ndarray, k: int = 3):
    assert k % 2 == 1
    n = len(a)
    mitad = k//2
    return [
        float(np.sum(a[i - mitad: i + mitad + 1]))
        for i in range(mitad, n - mitad)
    ]

def p2_gen(a: np.ndarray, k: int = 3):
    assert k % 2 == 1
    n = len(a)
    mitad = k//2
    for i in range(mitad, n - mitad):
        yield float(np.sum(a[i - mitad: i + mitad + 1]))

def p2_np(a: np.ndarray, k: int = 3):
    assert k % 2 == 1
    n = len(a)
    mitad = k // 2
    offsets = range(-mitad, mitad+1)
    slices = [a[mitad + off:n - mitad + off] for off in offsets]
    stacked = np.vstack(slices)
    return stacked.sum(axis=0)

def tiempo_p2(n=100_000, number=3):
    a = np.arange(n, dtype=float)
    k = 3
    return (
        timeit.timeit(lambda: p2_for(a, k), number=number),
        timeit.timeit(lambda: p2_comp(a, k), number=number),
        timeit.timeit(lambda: list(p2_gen(a, k)), number=number),
        timeit.timeit(lambda: p2_np(a, k), number=number),
    )

# Problema 3

def p3_for(a: np.ndarray, umbral: float):
    resultado = []
    for x in a:
        t = math.sin(x) + x**2
        if t > umbral:
            resultado.append(t)
    return resultado

def p3_comp(a: np.ndarray, umbral: float):
    return [
        (math.sin(x) + x**2)
        for x in a
        if (math.sin(x) + x**2) > umbral
    ]

def p3_gen(a: np.ndarray, umbral: float):
    for x in a:
        t = math.sin(x) + x**2
        if t > umbral:
            yield t

def p3_np(a: np.ndarray, umbral: float):
    t = np.sin(a) + a**2
    mascara = t > umbral
    return t[mascara]

def tiempo_p3(n=200_000, number=3):
    a = np.linspace(0, 1000, n, dtype=float)
    umbral = 10.0
    return (
        timeit.timeit(lambda: p3_for(a, umbral), number=number),
        timeit.timeit(lambda: p3_comp(a, umbral), number=number),
        timeit.timeit(lambda: list(p3_gen(a, umbral)), number=number),
        timeit.timeit(lambda: p3_np(a, umbral), number=number),
    )

# Verificación de tiempos

def _check_p1():
    a = np.arange(10, dtype=float)
    c = 2.0
    r_for = np.array(p1_for(a, c))
    r_comp = np.array(p1_comp(a, c))
    r_gen = np.array(list(p1_gen(a, c)))
    r_np = p1_np(a, c)
    print("P1 iguales:",
          np.allclose(r_for, r_comp),
          np.allclose(r_for, r_gen),
          np.allclose(r_for, r_np))

def _check_p2():
    a = np.arange(10, dtype=float)
    k = 3
    r_for = np.array(p2_for(a, k))
    r_comp = np.array(p2_comp(a, k))
    r_gen = np.array(list(p2_gen(a, k)))
    r_np = p2_np(a, k)
    print("P2 iguales:",
          np.allclose(r_for, r_comp),
          np.allclose(r_for, r_gen),
          np.allclose(r_for, r_np))

def _check_p3():
    a = np.linspace(0, 100, 50, dtype=float)
    umbral = 10.0
    r_for = np.array(p3_for(a, umbral))
    r_comp = np.array(p3_comp(a, umbral))
    r_gen = np.array(list(p3_gen(a, umbral)))
    r_np = p3_np(a, umbral)
    print("P3 iguales:",
          np.allclose(r_for, r_comp),
          np.allclose(r_for, r_gen),
          np.allclose(r_for, r_np))

if __name__ == "__main__":
    _check_p1()
    _check_p2()
    _check_p3()
    print("P1 tiempos:", tiempo_p1())
    print("P2 tiempos:", tiempo_p2())
    print("P3 tiempos:", tiempo_p3())

def guardar_en_json():
    n1, n2_p2, n3 = 100_000, 100_000, 200_000
    number_p1, number_p2, number_p3 = 5, 3, 3

    t1 = tiempo_p1(n=n1, num=number_p1)
    t2 = tiempo_p2(n=n2_p2, number=number_p2)
    t3 = tiempo_p3(n=n3, number=number_p3)

    results = {
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "machine": platform.machine(),
            "params": {
                "p1": {"n": n1, "number": number_p1},
                "p2": {"n": n2_p2, "number": number_p2},
                "p3": {"n": n3, "number": number_p3},
            },
        },
        "results": {
            "p1": {
                "for":   {"s_total": t1[0], "repetitions": number_p1,
                          "s_per_call": t1[0] / number_p1},
                "comp":  {"s_total": t1[1], "repetitions": number_p1,
                          "s_per_call": t1[1] / number_p1},
                "gen":   {"s_total": t1[2], "repetitions": number_p1,
                          "s_per_call": t1[2] / number_p1},
                "numpy": {"s_total": t1[3], "repetitions": number_p1,
                          "s_per_call": t1[3] / number_p1},
            },
            "p2": {
                "for":   {"s_total": t2[0], "repetitions": number_p2,
                          "s_per_call": t2[0] / number_p2},
                "comp":  {"s_total": t2[1], "repetitions": number_p2,
                          "s_per_call": t2[1] / number_p2},
                "gen":   {"s_total": t2[2], "repetitions": number_p2,
                          "s_per_call": t2[2] / number_p2},
                "numpy": {"s_total": t2[3], "repetitions": number_p2,
                          "s_per_call": t2[3] / number_p2},
            },
            "p3": {
                "for":   {"s_total": t3[0], "repetitions": number_p3,
                          "s_per_call": t3[0] / number_p3},
                "comp":  {"s_total": t3[1], "repetitions": number_p3,
                          "s_per_call": t3[1] / number_p3},
                "gen":   {"s_total": t3[2], "repetitions": number_p3,
                          "s_per_call": t3[2] / number_p3},
                "numpy": {"s_total": t3[3], "repetitions": number_p3,
                          "s_per_call": t3[3] / number_p3},
            },
        },
    }

    import os
    base_dir = os.path.dirname(__file__)
    out_dir = os.path.join(base_dir, "results", "tiempos")
    os.makedirs(out_dir, exist_ok=True)

    filename = f"tiempos_p123_{datetime.utcnow().date().isoformat()}.json"
    out_path = os.path.join(out_dir, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("JSON guardado en:", out_path)

if __name__ == "__main__":
    _check_p1()
    _check_p2()
    _check_p3()
    guardar_en_json()
