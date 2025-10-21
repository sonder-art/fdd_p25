FROM python:3.13-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Instala uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copia requirements primero (para cache)
COPY requirements.txt /app/requirements.txt

# Crea venv con uv y actívalo en PATH
RUN uv venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"

# Instala dependencias (si está vacío, no truena)
RUN uv pip install --no-cache -r requirements.txt || true

# Copia el código
COPY labs/mystery /app/labs/mystery

# Ejecuta el programa
CMD ["python", "labs/mystery/main.py"]
