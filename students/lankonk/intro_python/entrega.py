import sys
from pathlib import Path

r = Path(__file__).with_name("notas.txt")

try:
    f = r.open("r",encoding="utf-8")
    txt = f.read()
    print(txt)
except FileNotFoundError:
    print("No se encontro el archivo")
    sys.exit(404)