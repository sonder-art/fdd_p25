FROM debian:12-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       ca-certificates openssh-client sshpass \
  && rm -rf /var/lib/apt/lists/*
COPY bandit_connect.sh /usr/local/bin/bandit_connect.sh
RUN chmod +x /usr/local/bin/bandit_connect.sh
ENV BANDIT_HOST=bandit.labs.overthewire.org \
    BANDIT_PORT=2220
ENTRYPOINT ["/usr/local/bin/bandit_connect.sh"]
