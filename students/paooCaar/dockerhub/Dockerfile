FROM python:3.13-slim

WORKDIR /app

# Instala sshpass y el cliente SSH (Debian/Ubuntu base)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sshpass openssh-client ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY run_bandit.sh /app/run_bandit.sh
RUN chmod +x /app/run_bandit.sh

# Variables por defecto (puedes sobreescribir en docker run)
ENV BANDIT_LEVEL=0
ENV BANDIT_PASS=bandit0

CMD ["./run_bandit.sh"]

