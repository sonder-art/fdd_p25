#!/usr/bin/env python3
"""
Script que lee y muestra el contenido de notas.txt
"""
import sys
import os

def main():
    """Función principal que lee e imprime notas.txt"""
    notas_file = 'notas.txt'

    try:
        # Verificar si el archivo existe
        if not os.path.exists(notas_file):
            print(f"ERROR: El archivo '{notas_file}' no existe en el directorio actual.", file=sys.stderr)
            sys.exit(1)

        # Abrir y leer el archivo
        with open(notas_file, 'r', encoding='utf-8') as file:
            contenido = file.read()
            print(contenido, end='')

    except FileNotFoundError:
        print(f"ERROR: No se pudo encontrar el archivo '{notas_file}'.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"ERROR: No hay permisos para leer '{notas_file}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR inesperado al leer '{notas_file}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
