# Dockerfile portable, sin BuildKit y multi-arch friendly
FROM python:3.12-slim

# Evita prompts y bytecode; salida no bufferizada
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Herramientas mínimas para instalar uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Instala uv en /root/.local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Carpeta de trabajo
WORKDIR /app

# Capa separada para cachear deps
COPY requirements.txt /app/requirements.txt

# Crea el venv en /opt/venv e instala dependencias usando uv
# Nota: uv venv no trae pip por defecto; por eso usamos uv pip apuntando al Python del venv
RUN uv venv /opt/venv \
 && uv pip install --python /opt/venv/bin/python -r /app/requirements.txt

# Copia el resto del proyecto (incluye labs/mystery/main.py)
COPY . /app

# Asegura que el venv esté al frente del PATH
ENV PATH="/opt/venv/bin:${PATH}"

# Ejecuta el script misterioso con el python del venv (ruta absoluta)
CMD ["/opt/venv/bin/python", "labs/mystery/main.py"]

