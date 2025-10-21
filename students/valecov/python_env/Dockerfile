# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el requirements.txt primero e instala dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto completo
COPY labs/mystery /app

# Comando por defecto
CMD ["python", "main.py"]

