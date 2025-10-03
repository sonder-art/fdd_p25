import math;

print("Este es mi primer script usando python")
w = math.sqrt(169)
print("La raíz de 169 es: ", w)

def suma_dif_producto(num1, num2):
    s = num1 + num2
    r = num1 - num2
    m = num1 * num2

    return s, r, m

suma, resta, multiplicacion = suma_dif_producto(10, 5)

print("-" * 25)
print("Para los números 10 y 5")
print("La suma es:", suma)
print("La resta es:", resta)
print("La multiplicación es:", multiplicacion)


