# Imagen base con Python 3 (ligera)
FROM python:3.12-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY entrega.py notas.txt ./

# Comando que ejecutará al iniciar el contenedor
CMD ["python", "entrega.py"]