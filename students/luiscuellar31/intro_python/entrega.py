#!/usr/bin/env python3
import os, sys

def main():
    base = os.path.dirname(__file__)
    path = os.path.join(base, "notas.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        sys.stderr.write("Error: 'notas.txt' no existe en el directorio actual.\n")
        sys.exit(1)
    print(content, end="")

if __name__ == "__main__":
    main()

