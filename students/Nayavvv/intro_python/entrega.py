#!/usr/bin/env python3
import sys
from pathlib import Path

def main() -> None:
    here = Path(__file__).parent
    notas = here / "notas.txt"
    try:
        text = notas.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("ERROR: no se encontró notas.txt en el mismo directorio que entrega.py.", file=sys.stderr)
        sys.exit(1)
    print(text, end="")

if __name__ == "__main__":
    main()
