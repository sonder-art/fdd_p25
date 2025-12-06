import sys


def main():
    file_path = "notas.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            contenido = f.read()
            print(contenido, end="")
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{file_path}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
