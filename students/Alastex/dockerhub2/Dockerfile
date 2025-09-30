FROM debian:bullseye

# 1. Instalar dependencias (esto casi nunca cambia)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ssh sshpass ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 2. Copiar el script (esto sí cambia seguido)
COPY bandit.sh /usr/local/bin/bandit.sh
RUN chmod +x /usr/local/bin/bandit.sh

# 3. Definir el entrypoint
ENTRYPOINT ["/usr/local/bin/bandit.sh"]

