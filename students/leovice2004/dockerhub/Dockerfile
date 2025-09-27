
FROM debian:bookworm-slim

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       bash \
       openssh-client \
       sshpass \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

WORKDIR /app

COPY --chown=appuser:appgroup conecta_bandit.sh /app/conecta_bandit.sh
RUN chmod +x /app/conecta_bandit.sh

USER appuser

ENTRYPOINT ["/bin/bash", "/app/conecta_bandit.sh"]

