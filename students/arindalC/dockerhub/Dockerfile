FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ssh sshpass ca-certificates bash && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY bandit.sh /app/bandit.sh
RUN chmod +x /app/bandit.sh
ENV BANDIT_PORT=2220
ENTRYPOINT ["/app/bandit.sh"]