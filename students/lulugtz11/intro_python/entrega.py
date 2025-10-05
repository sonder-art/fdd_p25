#!/usr/bin/env python3
from pathlib import Path
import sys

def main():
    base = Path(__file__).parent
    notas = base / "notas.txt"
    try:
        contenido = notas.read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.stderr.write("ERROR: no se encontró 'notas.txt' en el mismo directorio.\n")
        sys.exit(1)  # código != 0
    print(contenido, end="")  # imprimir TAL CUAL, sin líneas extra

if __name__ == "__main__":
    main()
