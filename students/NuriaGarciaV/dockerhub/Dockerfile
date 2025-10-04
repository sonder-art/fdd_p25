# Imagen base
FROM ubuntu:22.04

# Actualizar e instalar dependencias
RUN apt-get update && apt-get install -y \
    ssh \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el script al contenedor
COPY connect_bandit.sh /usr/local/bin/connect_bandit.sh

# Dar permisos de ejecución
RUN chmod +x /usr/local/bin/connect_bandit.sh

# Definir el comando por defecto al iniciar
CMD ["/usr/local/bin/connect_bandit.sh"]

