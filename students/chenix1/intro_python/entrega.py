import sys

try:
    with open('notas.txt', 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("Error: El archivo 'notas.txt' mo fue encontrado")
    sys.exit(1)

except Exception as e:
    print("ocurrio un error inesperado: {e}")
    sys.exit(1)

