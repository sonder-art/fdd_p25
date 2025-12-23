import sys

def main():
    try:
        with open("notas.txt", "r", encoding="utf-8") as f:
            contenido = f.read()
            print(contenido)
    except FileNotFoundError:
        print("Error: El archivo 'notas.txt' no se encuentra.")
        sys.exit(1)

if __name__ == "__main__":
    main()
