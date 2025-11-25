FROM debian:stable-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-client sshpass ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV BANDIT_HOST=bandit.labs.overthewire.org \
    BANDIT_PORT=2220

ENTRYPOINT ["/app/entrypoint.sh"]