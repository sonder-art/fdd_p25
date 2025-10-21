try:
    # Intentar abrir notas.txt en modo lectura
    with open("notas.txt", "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    print(contenido)

except FileNotFoundError:
    print("Error: el archivo 'notas.txt' no existe en este directorio.")
