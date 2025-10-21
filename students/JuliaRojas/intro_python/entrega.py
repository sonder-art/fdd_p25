import sys
nombre_archivo= "notas.txt"

try:
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
        print(contenido)

except FileNotFoungError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
        sys.exit(1)

