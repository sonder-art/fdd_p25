import sys
from pathlib import Path

P = Path(__file__).with_name("notas.txt")
try:
    data = P.read_text(encoding="utf-8")
except FileNotFoundError:
    print("ERROR: notas.txt no existe en el mismo directorio.", file=sys.stderr)
    sys.exit(1)

print(data, end="")  # imprime tal cual, sin agregar líneas
