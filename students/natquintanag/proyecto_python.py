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

#P1: Segundo ejericio

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


if __name__ == "__main__":
    n = 10_000
    a = np.arange(n, dtype=float)
    c = 2.0

    res_for = p1_for(a, c)
    res_comp = p1_comp(a, c)
    res_gen = np.fromiter(p1_gen(a, c), dtype=float)
    res_np = p1_np(a, c)

    print("p1_for vs p1_np:", np.allclose(res_for, res_np))
    print("p1_comp vs p1_np:", np.allclose(res_comp, res_np))
    print("p1_gen vs p1_np:", np.allclose(res_gen, res_np))

    print("\nTiempos P1 (for, comp, gen(list), numpy):")
    print(time_p1())