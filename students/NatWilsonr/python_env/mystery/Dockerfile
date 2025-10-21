#Imagen base de Python
FROM python:3.12-slim

#Configuraciones básicas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar curl para poder descargar uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar curl para poder descargar uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# Instalar uv (gestor rápido de paquetes Python)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos requirements.txt
COPY students/NatWilsonr/python_env/mystery/requirements.txt /app/requirements.txt

# Instalar dependencias si existen
RUN if [ -s requirements.txt ]; then uv pip install --system -r requirements.txt; fi

# Copiar el código del lab del profe
COPY professor/python_env/labs/mystery /app/labs/mystery

# Comando final que ejecuta el programa
CMD ["python", "labs/mystery/main.py"]
