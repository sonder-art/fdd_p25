FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-client sshpass ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY start-bandit.sh /usr/local/bin/start-bandit.sh
RUN chmod +x /usr/local/bin/start-bandit.sh

ENV BANDIT_LEVEL= \
    BANDIT_PASSWORD= \
    BANDIT_PORT=2220

ENTRYPOINT ["/usr/local/bin/start-bandit.sh"]
