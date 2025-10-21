FROM ubuntu:22.04

# Instalar dependencias necesarias
RUN apt-get update && \
    apt-get install -y \
    openssh-client \
    sshpass \
    && rm -rf /var/lib/apt/lists/*

# Copiar el script al contenedor
COPY bandit_connect.sh /usr/local/bin/bandit_connect.sh

# Dar permisos de ejecución al script
RUN chmod +x /usr/local/bin/bandit_connect.sh

# Definir variables de entorno por defecto (opcionales)
ENV BANDIT_LEVEL=""
ENV BANDIT_PASSWORD=""

# Ejecutar el script al iniciar el contenedor
ENTRYPOINT ["/usr/local/bin/bandit_connect.sh"]
