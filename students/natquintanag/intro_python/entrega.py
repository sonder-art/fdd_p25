from pathlib import Path
import sys

ruta = Path(__file__).with_name("notas.txt")

try:
    
    with ruta.open("r", encoding="utf-8") as f:
        contenido = f.read()
    
    print(contenido, end="")

except FileNotFoundError:
    print("ERROR: no se encontró 'notas.txt' en el mismo directorio.", file=sys.stderr)
    sys.exit(1)
