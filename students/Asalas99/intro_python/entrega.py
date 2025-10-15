import sys

try:
    with open('notas.txt', 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        print(contenido, end='')
except FileNotFoundError:
    print("ERROR: El archivo 'notas.txt' no existe en el directorio actual.", file=sys.stderr)
    sys.exit(1)

