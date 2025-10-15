# Dockerfile
FROM debian:latest

# Instalar dependencias necesarias: ssh y sshpass
RUN apt-get update && apt-get install -y \
    openssh-client \
    sshpass \
    && rm -rf /var/lib/apt/lists/*

# Definir carpeta de trabajo
WORKDIR /app

# Copiar el script al contenedor
COPY script.sh /app/script.sh

# Darle permisos de ejecución
RUN chmod +x /app/script.sh

# Al arrancar el contenedor, se ejecuta el script
ENTRYPOINT ["/app/script.sh"]

