#!/usr/bin/env python3
import sys
import os

RUTA_NOTAS = "notas.txt"

if not os.path.exists(RUTA_NOTAS):
    print("Error: el archivo 'notas.txt' no existe.", file=sys.stderr)
    sys.exit(1)

with open(RUTA_NOTAS, "r", encoding="utf-8") as f:
    contenido = f.read().strip()
    if contenido:
        print("Contenido de notas.txt:\n")
        print(contenido)
    else:
        print("El archivo 'notas.txt' está vacío.")

