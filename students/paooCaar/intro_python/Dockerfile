# Imagen base de Python 3
FROM python:3.13-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos necesarios al contenedor
COPY entrega.py notas.txt ./

# Comando por defecto: ejecutar entrega.py
CMD ["python3", "entrega.py"]
