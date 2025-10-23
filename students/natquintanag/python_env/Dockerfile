FROM python:3.12-slim

# Instalar uv
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copiar primero requirements para cache
COPY students/natquintanag/python_env/requirements.txt /app/requirements.txt

# Crear venv con uv e instalar (si el archivo no está vacío)
RUN uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN if [ -s /app/requirements.txt ]; then uv pip install -r /app/requirements.txt; fi

# Copiar todo el repo (necesitamos labs/mystery/main.py)
COPY . /app

# Ejecutar el script del lab
CMD ["python", "students/natquintanag/python_env/labs/mystery/main.py"]
