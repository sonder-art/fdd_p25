# Imagen base de Python 3
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos necesarios al contenedor
COPY entrega.py notas.txt /app/

# Comando por defecto: ejecutar el script
CMD ["python", "entrega.py"]
