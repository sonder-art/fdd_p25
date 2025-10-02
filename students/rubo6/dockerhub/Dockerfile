FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      openssh-client sshpass ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENV BANDIT_LEVEL="" \
    BANDIT_PASSWORD=""
ENTRYPOINT ["/app/entrypoint.sh"]
