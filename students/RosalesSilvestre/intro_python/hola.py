#!/usr/bin/env python3
"""
Script mínimo de ejemplo para el ejercicio intro_python
"""

# 1. Un print() con un saludo
print("¡Hola desde Python!")

# 2. Una variable con el resultado de una operación aritmética y un print() mostrando ese resultado
resultado = 15 * 3
print(f"El resultado de 15 * 3 es: {resultado}")

# 3. Una función simple y un print() mostrando la llamada a esa función con un valor
def duplicar(numero):
    """Duplica un número"""
    return numero * 2

valor_duplicado = duplicar(7)
print(f"El doble de 7 es: {valor_duplicado}")

