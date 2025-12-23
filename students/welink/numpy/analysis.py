import numpy as np
import pandas as pd

def main():
    print("--- Numpy ---")
    # Crear arrays
    vector = np.array([1, 2, 3, 4, 5])
    matriz = np.array([[1, 2], [3, 4]])
    
    print(f"Vector: {vector}")
    print(f"Matriz:\n{matriz}")
    
    # Operaciones
    print(f"Suma del vector: {np.sum(vector)}")
    print(f"Media del vector: {np.mean(vector)}")
    print(f"Producto punto (v*v): {np.dot(vector, vector)}")

    print("\n--- Pandas ---")
    # Crear DataFrame
    data = {
        'Nombre': ['Ana', 'Luis', 'Marta', 'Pedro'],
        'Edad': [23, 30, 21, 35],
        'Ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia']
    }
    df = pd.DataFrame(data)
    print("DataFrame original:")
    print(df)

    # Filtrar
    filtro = df[df['Edad'] > 25]
    print("\nPersonas mayores de 25:")
    print(filtro)

    # Estadísticas
    print("\nEstadísticas descriptivas:")
    print(df.describe())

if __name__ == "__main__":
    main()
