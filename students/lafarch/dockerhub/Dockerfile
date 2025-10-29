FROM ubuntu:22.04

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar e instalar SSH client y sshpass
RUN apt-get update && \
    apt-get install -y \
    openssh-client \
    sshpass && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar el script al contenedor
COPY connect_bandit.sh /usr/local/bin/connect_bandit.sh

# Dar permisos de ejecución
RUN chmod +x /usr/local/bin/connect_bandit.sh

# Establecer el script como punto de entrada
ENTRYPOINT ["/usr/local/bin/connect_bandit.sh"]
