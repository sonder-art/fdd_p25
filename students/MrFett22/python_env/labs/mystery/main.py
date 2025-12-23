import os
import sys


def main() -> int:
    # Objetivo del reto: que este programa imprima un mensaje "bonito" y termine con 0.
    # Pistas mínimas: el código intenta usar librerías externas comunes, pero no se listan aquí.
    # El alumnado debe descubrirlas según los errores que aparezcan en tiempo de ejecución.

    # 1) Usa variables de entorno y una librería externa para dar color/estilo al texto.
    # 2) Hace una petición HTTP simple (solo GET) para obtener un dato público.
    # 3) Formatea una pequeña tabla en salida estándar.

    # Nota: no importamos arriba para que los errores muestren claramente qué falta.
    try:
        # colores bonitos
        from rich import print as rprint  # type: ignore
        from rich.table import Table  # type: ignore
    except Exception as exc:
        sys.stderr.write("Falta una dependencia para salida formateada.\n")
        raise

    try:
        # http cliente
        import httpx  # type: ignore
    except Exception:
        sys.stderr.write("Falta una dependencia para hacer requests HTTP.\n")
        raise

    # Fuente de datos: un endpoint público muy simple
    url = os.environ.get("MYSTERY_URL", "https://httpbin.org/uuid")

    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        sys.stderr.write("No se pudo obtener/parsear el JSON del endpoint.\n")
        raise

    # Construir una tabla mínima
    table = Table(title="Mystery App — Resultado")
    table.add_column("Clave", style="cyan", no_wrap=True)
    table.add_column("Valor", style="magenta")

    # Muestra 1–2 campos si existen; el objetivo no es el contenido, sino que corra
    for key in ("uuid",):
        value = data.get(key, "<no disponible>") if isinstance(data, dict) else "<no dict>"
        table.add_row(key, str(value))

    rprint(table)
    rprint("[green]OK[/green] — entorno configurado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


