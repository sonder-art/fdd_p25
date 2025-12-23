import os
import datetime

def main():
    print("Hola desde Docker!")
    
    # Escribir en un archivo dentro del volumen (si existe)
    data_dir = "/app/data"
    if os.path.exists(data_dir):
        timestamp = datetime.datetime.now().isoformat()
        file_path = os.path.join(data_dir, "log.txt")
        with open(file_path, "a") as f:
            f.write(f"Ejecución a las {timestamp}\n")
        print(f"Se ha escrito un log en {file_path}")
    else:
        print(f"El directorio {data_dir} no existe. Monta un volumen para persistencia.")

if __name__ == "__main__":
    main()
