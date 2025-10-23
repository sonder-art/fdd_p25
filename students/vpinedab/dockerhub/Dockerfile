FROM debian:12-slim

# Instala cliente SSH y sshpass para pasar password de forma no interactiva
RUN apt-get update && apt-get install -y openssh-client sshpass

WORKDIR /app
COPY run_bandit.sh /usr/local/bin/run_bandit.sh
RUN chmod +x /usr/local/bin/run_bandit.sh

# Al iniciar el contenedor, se ejecuta el script
ENTRYPOINT ["/usr/local/bin/run_bandit.sh"]
# Si pasas argumentos a `docker run`, se le agregan al script como "$@"
