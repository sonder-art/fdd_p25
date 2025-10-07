# 1. Imagen base
FROM python:3.12-slim

# 2. Instalar uv
RUN pip install uv

# 3. Directorio de trabajo
WORKDIR /app

# 4. Copiar el código
COPY . .

# 5. Instalar dependencias
RUN uv pip install --system -r requirements.txt


# 6. Comando por defecto
CMD ["python", "main.py"]
 
