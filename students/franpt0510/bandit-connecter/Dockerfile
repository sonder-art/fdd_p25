# Imagen base mínima
FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    sshpass \
    bash \
    tini \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENV BANDIT_HOST=bandit.labs.overthewire.org \
    BANDIT_PORT=2220
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]

CMD []

