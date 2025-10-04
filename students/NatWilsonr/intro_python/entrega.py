import sys

try:
    with open("notas.txt", encoding="utf-8") as f:
        print(f.read(), end="")
except FileNotFoundError:
    print("Error: falta 'notas.txt' junto a 'entrega.py'.", file=sys.stderr)
    sys.exit(1)
