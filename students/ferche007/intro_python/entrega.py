import sys

try:
    with open("notas.txt", "r", encoding="utf-8") as f:
        sys.stdout.write(f.read())
except FileNotFoundError:
    print("Error: no se encontró 'notas.txt' en este directorio.", file=sys.stderr)
    sys.exit(1)

