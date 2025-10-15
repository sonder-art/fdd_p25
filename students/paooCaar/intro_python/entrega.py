import sys

def main():
    try:
        with open("notas.txt", "r", encoding="utf-8") as f:
            contenido = f.read()
        # Imprimir TAL CUAL, sin agregar ni quitar líneas
        print(contenido, end="")
    except FileNotFoundError:
        print("ERROR: notas.txt no existe en el directorio actual.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()


