#!/usr/bin/env python3
import sys
from pathlib import Path

ruta_notas = Path(__file__).with_name("notas.txt")

try:

    contenido = ruta_notas.read_text(encoding="utf-8")
    print(contenido, end="")

except FileNotFoundError:
    
    sys.stderr.write("ERROR: No se encontró el archivo notas.txt en este directorio.\n")
    sys.exit(1)