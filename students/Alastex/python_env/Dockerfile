FROM python:3.11-slim

# Instalar uv (administrador de dependencias ultrarrápido)
RUN pip install uv

WORKDIR /app

# Copiamos el código del lab y el requirements.txt
COPY requirements.txt .

# Instalamos dependencias con uv
RUN uv pip install -r requirements.txt

COPY labs/ ./labs/
# Comando de arranque
CMD ["python", "labs/mystery/main.py"]
