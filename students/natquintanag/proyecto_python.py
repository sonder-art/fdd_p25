import numpy as np
import timeit

#P1 Primer ejericio
def p1_for(a: np.ndarray, c: float) -> np.ndarray:
    """
    Devuelve a*c usando un for y append sobre una lista
    y luego lo convierte a np.ndarray.
    """
    resultado = []
    for x in a:
        resultado.append(x * c)
    return np.array(resultado, dtype=float)


def p1_comp(a: np.ndarray, c: float) -> np.ndarray:
    """
    Devuelve a*c usando list comprehension
    y lo convierte a np.ndarray.
    """
    return np.array([x * c for x in a], dtype=float)


def p1_gen(a: np.ndarray, c: float):
    """
    Devuelve un generador que produce los elementos de a*c.
    Para compararlo con las otras versiones, se debe materializar:
        list(p1_gen(a, c))  o  np.fromiter(p1_gen(a, c), float)
    """
    return (x * c for x in a)


def p1_np(a: np.ndarray, c: float) -> np.ndarray:
    """
    Devuelve a*c usando NumPy vectorizado.
    """
    return a * c

#P1 Segundo ejercicio
def time_p1(n=100_000, number=5):
    """
    Mide tiempos de las 4 estrategias para P1.
    Regresa una tupla: (for, comp, gen, numpy)
    con el tiempo total de 'number' repeticiones.
    """
    a = np.arange(n, dtype=float)
    c = 2.0

    return (
        timeit.timeit(lambda: p1_for(a, c), number=number),
        timeit.timeit(lambda: p1_comp(a, c), number=number),
        timeit.timeit(lambda: list(p1_gen(a, c)), number=number),
        timeit.timeit(lambda: p1_np(a, c), number=number),
    )

# P2 Primer ejercicio
def p2_for(a: np.ndarray, k: int = 3) -> np.ndarray:
    """
    Devuelve la suma de vecinos con ventana de tamaño k (impar >= 3)
    usando un for clásico.

    Política de bordes:
    - Solo se consideran ventanas COMPLETAS.
    - La salida tiene longitud n - k + 1.
    """
    if k % 2 == 0 or k < 3:
        raise ValueError("k debe ser impar y >= 3")

    n = len(a)
    half = k // 2
    resultado = []

    for i in range(half, n - half):
        ventana = a[i - half : i + half + 1]
        resultado.append(float(np.sum(ventana)))

    return np.array(resultado, dtype=float)


def p2_comp(a: np.ndarray, k: int = 3) -> np.ndarray:
    """
    Versión con list comprehension.
    Misma política de bordes que p2_for.
    """
    if k % 2 == 0 or k < 3:
        raise ValueError("k debe ser impar y >= 3")

    n = len(a)
    half = k // 2

    return np.array(
        [
            float(np.sum(a[i - half : i + half + 1]))
            for i in range(half, n - half)
        ],
        dtype=float,
    )


def p2_gen(a: np.ndarray, k: int = 3):
    """
    Versión con generador.
    Misma política de bordes.
    """
    if k % 2 == 0 or k < 3:
        raise ValueError("k debe ser impar y >= 3")

    n = len(a)
    half = k // 2

    for i in range(half, n - half):
        yield float(np.sum(a[i - half : i + half + 1]))


def p2_np(a: np.ndarray, k: int = 3) -> np.ndarray:
    """
    Versión NumPy vectorizada usando convolución simple.
    mode='valid' asegura windows completas.
    """
    if k % 2 == 0 or k < 3:
        raise ValueError("k debe ser impar y >= 3")

    kernel = np.ones(k, dtype=float)
    return np.convolve(a, kernel, mode="valid")

# P2 Segundo ejercicio
def time_p2(n=100_000, number=3):
    """
    Mide tiempos de las 4 estrategias para P2.
    """
    a = np.arange(n, dtype=float)
    k = 3

    return (
        timeit.timeit(lambda: p2_for(a, k), number=number),
        timeit.timeit(lambda: p2_comp(a, k), number=number),
        timeit.timeit(lambda: list(p2_gen(a, k)), number=number),
        timeit.timeit(lambda: p2_np(a, k), number=number),
    )

# Main

if __name__ == "__main__":
    # Pruebas P1
    n = 10_000
    a = np.arange(n, dtype=float)
    c = 2.0

    res_for = p1_for(a, c)
    res_comp = p1_comp(a, c)
    res_gen = np.fromiter(p1_gen(a, c), dtype=float)
    res_np = p1_np(a, c)

    print("P1 — equivalencia de resultados:")
    print("p1_for  vs p1_np:", np.allclose(res_for, res_np))
    print("p1_comp vs p1_np:", np.allclose(res_comp, res_np))
    print("p1_gen  vs p1_np:", np.allclose(res_gen, res_np))

    print("\nTiempos P1 (for, comp, gen(list), numpy):")
    print(time_p1())

    # Pruebas P2

    k = 3

    b_for = p2_for(a, k)
    b_comp = p2_comp(a, k)
    b_gen = np.fromiter(p2_gen(a, k), dtype=float)
    b_np = p2_np(a, k)

    print("\nP2 — equivalencia de resultados:")
    print("p2_for  vs p2_np:", np.allclose(b_for, b_np))
    print("p2_comp vs p2_np:", np.allclose(b_comp, b_np))
    print("p2_gen  vs p2_np:", np.allclose(b_gen, b_np))

    print("\nTiempos P2 (for, comp, gen(list), numpy):")
    print(time_p2())

# P3 Primer ejercicio
def p3_for(a: np.ndarray, umbral: float) -> np.ndarray:
    """
    Aplica sin(x) + x**2 y filtra los valores > umbral usando un for.
    Devuelve un np.ndarray con los valores transformados que pasan el filtro.
    """
    resultado = []
    for x in a:
        val = np.sin(x) + x**2
        if val > umbral:
            resultado.append(float(val))
    return np.array(resultado, dtype=float)


def p3_comp(a: np.ndarray, umbral: float) -> np.ndarray:
    """
    Versión con list comprehension.
    """
    return np.array(
        [
            float(np.sin(x) + x**2)
            for x in a
            if (np.sin(x) + x**2) > umbral
        ],
        dtype=float,
    )


def p3_gen(a: np.ndarray, umbral: float):
    """
    Versión con generador.
    Para compararla:
        list(p3_gen(a, umbral))  o  np.fromiter(p3_gen(a, umbral), float)
    """
    for x in a:
        val = np.sin(x) + x**2
        if val > umbral:
            yield float(val)


def p3_np(a: np.ndarray, umbral: float) -> np.ndarray:
    """
    Versión NumPy vectorizada:
    - Usa ufuncs (np.sin, **2)
    - Aplica máscara booleana > umbral
    """
    vals = np.sin(a) + a**2
    mask = vals > umbral
    return vals[mask]

# P3 Segundo ejercicio
def time_p3(n=200_000, number=3):
    """
    Mide tiempos de las 4 estrategias para P3.
    """
    a = np.linspace(0, 1000, n, dtype=float)
    umbral = 10.0

    return (
        timeit.timeit(lambda: p3_for(a, umbral), number=number),
        timeit.timeit(lambda: p3_comp(a, umbral), number=number),
        timeit.timeit(lambda: list(p3_gen(a, umbral)), number=number),
        timeit.timeit(lambda: p3_np(a, umbral), number=number),
    )

# Main
if __name__ == "__main__":
    # Pruebas P1
    n = 10_000
    a = np.arange(n, dtype=float)
    c = 2.0

    res_for = p1_for(a, c)
    res_comp = p1_comp(a, c)
    res_gen = np.fromiter(p1_gen(a, c), dtype=float)
    res_np = p1_np(a, c)

    print("P1 — equivalencia de resultados:")
    print("p1_for  vs p1_np:", np.allclose(res_for, res_np))
    print("p1_comp vs p1_np:", np.allclose(res_comp, res_np))
    print("p1_gen  vs p1_np:", np.allclose(res_gen, res_np))

    print("\nTiempos P1 (for, comp, gen(list), numpy):")
    print(time_p1())

    # Pruebas P2
    k = 3

    b_for = p2_for(a, k)
    b_comp = p2_comp(a, k)
    b_gen = np.fromiter(p2_gen(a, k), dtype=float)
    b_np = p2_np(a, k)

    print("\nP2 — equivalencia de resultados:")
    print("p2_for  vs p2_np:", np.allclose(b_for, b_np))
    print("p2_comp vs p2_np:", np.allclose(b_comp, b_np))
    print("p2_gen  vs p2_np:", np.allclose(b_gen, b_np))

    print("\nTiempos P2 (for, comp, gen(list), numpy):")
    print(time_p2())

    # Pruebas P3
    a3 = np.linspace(0, 1000, 50_000, dtype=float)
    umbral = 10.0

    c_for = p3_for(a3, umbral)
    c_comp = p3_comp(a3, umbral)
    c_gen = np.fromiter(p3_gen(a3, umbral), dtype=float)
    c_np = p3_np(a3, umbral)

    print("\nP3 — equivalencia de resultados:")
    print("p3_for  vs p3_np:", np.allclose(c_for, c_np))
    print("p3_comp vs p3_np:", np.allclose(c_comp, c_np))
    print("p3_gen  vs p3_np:", np.allclose(c_gen, c_np))

    print("\nTiempos P3 (for, comp, gen(list), numpy):")
    print(time_p3())