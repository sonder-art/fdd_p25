# Usa una imagen base con Python 3
FROM python:3.13-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY notas.txt entrega.py ./

# Indica el comando a ejecutar al iniciar el contenedor
CMD ["python", "entrega.py"]
