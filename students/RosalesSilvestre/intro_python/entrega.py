#!/usr/bin/env python3
"""
Script que lee y muestra el contenido de notas.txt
"""

import sys
import os


def main():
    """Lee notas.txt y lo imprime por pantalla"""
    # Obtener el directorio donde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notas_path = os.path.join(script_dir, "notas.txt")
    
    try:
        with open(notas_path, "r", encoding="utf-8") as f:
            contenido = f.read()
        print(contenido, end="")
        return 0
    except FileNotFoundError:
        sys.stderr.write(f"Error: No se encontró el archivo notas.txt en {script_dir}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error al leer notas.txt: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())

