FROM python:3.12-slim

# Instalar curl para instalar uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instalar uv y dejarlo accesible (sin -y)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

# Copia requirements si existe (cache de capas)
COPY requirements.txt /app/requirements.txt

# Crear venv + instalar deps con uv (si hay requirements con contenido)
RUN uv venv /app/.venv && . /app/.venv/bin/activate && \
    if [ -s /app/requirements.txt ]; then uv pip install -r /app/requirements.txt; fi

# Copiar el código (en este contexto, main.py queda en /app/main.py)
COPY . /app

# Ejecutar usando el Python del venv
CMD ["/app/.venv/bin/python", "main.py"]
