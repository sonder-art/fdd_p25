FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Instala uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && ln -s /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

# Cache de deps
COPY students/arindalC/python_env/requirements.txt /app/requirements.txt

RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/pip \
    uv pip install -r /app/requirements.txt

# Copia el lab mystery
COPY students/arindalC/python_env/labs/mystery /app/labs/mystery

# URL por variable de entorno
ENV MYSTERY_URL="https://httpbin.org/uuid"

CMD ["uv", "run", "labs/mystery/main.py"]