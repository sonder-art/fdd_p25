import sys

try:
    with open("notas.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
    sys.stdout.write(contenido)
except FileNotFoundError:
    sys.stderr.write("Error: notas.txt no existe en el directorio actual.\n")
    sys.exit(1)

