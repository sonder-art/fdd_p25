import sys

try:
        with open("notas.txt", "r") as f:
            contenido = f.read()
            print(contenido)
except FileNotFoundError:
        print("Error: el archivo notas.txt no existe.")
        sys.exit(1)
