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
COPY bandit_connect.sh /app/bandit_connect.sh

# Darle permisos de ejecución
RUN chmod +x /app/bandit_connect.sh

# Al arrancar el contenedor, se ejecuta el script
ENTRYPOINT ["/app/bandit_connect.sh"]