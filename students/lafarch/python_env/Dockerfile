# Dockerfile sugerido
FROM python:3.11-slim

# Instalar uv
RUN pip install uv

# Copiar archivos
WORKDIR /app
COPY labs/mystery/main.py labs/mystery/main.py
COPY requirements.txt .

# Crear ambiente virtual e instalar dependencias con uv
RUN uv venv .venv
RUN uv pip install -r requirements.txt

# Ejecutar el programa
CMD [".venv/bin/python", "labs/mystery/main.py"]
