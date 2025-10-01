import sys


try:    
    with open("notas.txt", "r") as archivo:
        contenido = archivo.read()
    
    print(contenido, end="")

except FileNotFoundError:
    
    # Imprime el mensaje de error solicitado
    print("Error: El archivo notas.txt no existe en el directorio actual.", file=sys.stderr)
    
    # Termina el programa
    sys.exit(1)
