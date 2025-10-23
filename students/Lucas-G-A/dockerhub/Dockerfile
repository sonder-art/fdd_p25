FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-client sshpass ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY run_bandit.sh /app/run_bandit.sh
RUN chmod +x /app/run_bandit.sh

ENTRYPOINT ["/app/run_bandit.sh"]

