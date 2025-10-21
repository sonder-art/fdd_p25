# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Instala uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copiamos SOLO tu requirements.txt (de TU carpeta en labs/mystery)
COPY students/rubo6/python_env/labs/mystery/requirements.txt /app/requirements.txt

# Creamos venv con uv e instalamos lo declarado (si está vacío, sigue)
RUN uv venv /opt/venv && . /opt/venv/bin/activate && \
    ( [ -s /app/requirements.txt ] && uv pip install -r /app/requirements.txt || true)

# Copiamos el código del profe SIN modificarlo
COPY professor/python_env/labs/mystery /app/labs/mystery

# Usar python del venv
ENV PATH="/opt/venv/bin:${PATH}"

# Ejecutar EXACTAMENTE esto (como pide el README)
CMD ["python", "labs/mystery/main.py"]
