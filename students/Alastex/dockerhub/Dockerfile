# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero el archivo de requisitos (para aprovechar cache)
COPY requirements.txt .

# Instala las dependencias necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends ssh sshpass ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copia todo el código al contenedor
COPY . /app

# Da permisos de ejecución al script
RUN chmod +x /app/bandit.sh

# Define el comando por defecto
CMD ["/app/bandit.sh"]
