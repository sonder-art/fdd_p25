FROM python:3.11-slim

# Instalar uv
RUN pip install --no-cache-dir uv

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias con uv
RUN uv pip install --system -r requirements.txt

# Copiar el código de la aplicación
COPY main.py .

# Ejecutar el script mystery
CMD ["python", "main.py"]

