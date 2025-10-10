FROM ubuntu:22.04

RUN apt-get update && apt-get install -y sshpass

COPY conexion_bandit.sh /tmp/conexion_bandit.sh

RUN chmod +x /tmp/conexion_bandit.sh

CMD ["/bin/bash"]