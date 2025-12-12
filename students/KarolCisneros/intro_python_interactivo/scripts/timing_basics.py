import argparse
import time
import timeit
from statistics import mean, stdev


def format_stats(samples: list[float]) -> str:
    if not samples:
        return "no samples"
    if len(samples) == 1:
        return f"{samples[0]*1000:.3f} ms"
    return f"{mean(samples)*1000:.3f} ms ± {stdev(samples)*1000:.3f} ms"


def bench_sum_builtin(n: int, repeat: int, number: int) -> list[float]:
    return timeit.repeat(lambda: sum(range(n)), number=number, repeat=repeat)


def bench_sum_loop(n: int, repeat: int, number: int) -> list[float]:
    def _f() -> int:
        total = 0
        for i in range(n):
            total += i
        return total

    return timeit.repeat(_f, number=number, repeat=repeat)


def bench_list_comp_vs_append(n: int, repeat: int, number: int) -> tuple[list[float], list[float]]:
    comp = timeit.repeat(lambda: [i * i for i in range(n)], number=number, repeat=repeat)

    def _append() -> list[int]:
        values: list[int] = []
        for i in range(n):
            values.append(i * i)
        return values

    app = timeit.repeat(_append, number=number, repeat=repeat)
    return comp, app


def bench_concat_vs_join(k: int, repeat: int, number: int) -> tuple[list[float], list[float]]:
    # k menor porque concatenar en bucle es O(n^2)
    def _concat() -> str:
        s = ""
        for _ in range(k):
            s += "a"
        return s

    def _join() -> str:
        return "".join(["a"] * k)

    concat = timeit.repeat(_concat, number=number, repeat=repeat)
    join = timeit.repeat(_join, number=number, repeat=repeat)
    return concat, join


def bench_set_vs_list_membership(n: int, repeat: int, number: int) -> tuple[list[float], list[float]]:
    universe = list(range(n))
    probe_values = list(range(n, n + 1000))  # misses para medir peor caso

    def _list_in() -> bool:
        found = False
        for x in probe_values:
            if x in universe:
                found = True
        return found

    def _set_in() -> bool:
        s = set(universe)
        found = False
        for x in probe_values:
            if x in s:
                found = True
        return found

    list_times = timeit.repeat(_list_in, number=number, repeat=repeat)
    set_times = timeit.repeat(_set_in, number=number, repeat=repeat)
    return list_times, set_times


def bench_any_vs_loop(n: int, repeat: int, number: int) -> tuple[list[float], list[float]]:
    data = [0] * (n - 1) + [1]

    def _loop() -> bool:
        for x in data:
            if x:
                return True
        return False

    loop_t = timeit.repeat(_loop, number=number, repeat=repeat)
    any_t = timeit.repeat(lambda: any(data), number=number, repeat=repeat)
    return any_t, loop_t


def print_header(title: str) -> None:
    print("\n" + title)
    print("-" * len(title))


def main() -> None:
    parser = argparse.ArgumentParser(description="Pequeñas comparaciones de rendimiento en Python (didácticas)")
    parser.add_argument(
        "--benchmark",
        choices=[
            "all",
            "sum",
            "list",
            "string",
            "membership",
            "any",
        ],
        default="all",
        help="Qué comparar",
    )
    parser.add_argument("--n", type=int, default=200_000, help="Tamaño del problema (depende de la prueba)")
    parser.add_argument("--repeat", type=int, default=5, help="Repeticiones para estadística")
    parser.add_argument("--number", type=int, default=1, help="Ejecuciones por repetición (timeit)")
    args = parser.parse_args()

    # Sumas
    if args.benchmark in ("all", "sum"):
        print_header("Suma: builtin sum vs bucle explícito")
        b = bench_sum_builtin(args.n, args.repeat, args.number)
        l = bench_sum_loop(args.n, args.repeat, args.number)
        print(f"sum(range(n)): {format_stats(b)}")
        print(f"for ... total += i: {format_stats(l)}")
        print(f"→ speedup (builtin / loop): {mean(l)/mean(b):.2f}× más rápido (aprox.)")

    # Listas
    if args.benchmark in ("all", "list"):
        print_header("Listas: comprensión vs append en bucle")
        comp, app = bench_list_comp_vs_append(args.n, args.repeat, args.number)
        print(f"[i*i for i in range(n)]: {format_stats(comp)}")
        print(f"append en bucle:            {format_stats(app)}")
        print(f"→ speedup (comp / append): {mean(app)/mean(comp):.2f}× más rápido (aprox.)")

    # Cadenas (k suele ser menor que n)
    if args.benchmark in ("all", "string"):
        k = max(10_000, min(args.n, 200_000))
        print_header(f"Cadenas: concatenar (+) vs join (k={k})")
        concat, join = bench_concat_vs_join(k, args.repeat, args.number)
        print(f"s += 'a': {format_stats(concat)}")
        print(f"''.join([...]): {format_stats(join)}")
        print(f"→ speedup (join / concat): {mean(concat)/mean(join):.2f}× más rápido (aprox.)")

    # Pertenencia
    if args.benchmark in ("all", "membership"):
        print_header("Pertenencia: list vs set (misses)")
        list_t, set_t = bench_set_vs_list_membership(args.n, args.repeat, args.number)
        print(f"x in list: {format_stats(list_t)}")
        print(f"x in set:  {format_stats(set_t)}")
        print(f"→ speedup (set / list): {mean(list_t)/mean(set_t):.2f}× más rápido (aprox.)")

    # any()
    if args.benchmark in ("all", "any"):
        print_header("any() vs bucle con return temprano")
        any_t, loop_t = bench_any_vs_loop(args.n, args.repeat, args.number)
        print(f"any(data):    {format_stats(any_t)}")
        print(f"loop+return:  {format_stats(loop_t)}")
        print(f"→ speedup (any / loop): {mean(loop_t)/mean(any_t):.2f}× más rápido (aprox.)")

    # Nota: Los resultados dependen de n, de la máquina y del intérprete.
    # El objetivo es observar tendencias y fomentar el pensamiento crítico.


if __name__ == "__main__":
    main()
