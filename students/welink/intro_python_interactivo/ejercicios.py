import math

def calcular_area_circulo(radio):
    return math.pi * (radio ** 2)

def main():
    # Estructuras de Control
    try:
        numero = int(input("Introduce un número: "))
        if numero % 2 == 0:
            print(f"El número {numero} es par.")
        else:
            print(f"El número {numero} es impar.")
    except ValueError:
        print("Eso no es un número válido.")

    print("\nContando del 1 al 10:")
    for i in range(1, 11):
        print(i, end=" ")
    print("\n")

    # Funciones
    radio = 5
    area = calcular_area_circulo(radio)
    print(f"El área de un círculo con radio {radio} es: {area:.2f}")

    # Listas
    frutas = ["manzana", "banana", "cereza", "dátil"]
    print("\nLista de frutas:")
    for fruta in frutas:
        print(f"- {fruta}")

    # Diccionarios
    persona = {
        "nombre": "Juan Pérez",
        "edad": 30,
        "ciudad": "México"
    }
    print("\nDatos de la persona:")
    for clave, valor in persona.items():
        print(f"{clave.capitalize()}: {valor}")

if __name__ == "__main__":
    main()
