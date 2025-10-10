FROM debian:stable-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client sshpass ca-certificates bash \
 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 appuser
USER appuser
WORKDIR /home/appuser
COPY --chown=appuser:appuser entrypoint.sh /home/appuser/entrypoint.sh
RUN chmod +x /home/appuser/entrypoint.sh
ENV BANDIT_LEVEL="" \
    BANDIT_PASSWORD="" \
    BANDIT_HOST="bandit.labs.overthewire.org" \
    BANDIT_PORT="2220" \
    BANDIT_COMMAND=""
ENTRYPOINT ["/home/appuser/entrypoint.sh"]
