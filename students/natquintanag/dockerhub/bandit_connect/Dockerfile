FROM alpine:3.20
RUN apk add --no-cache bash openssh-client sshpass
WORKDIR /app
COPY start_bandit.sh /usr/local/bin/start_bandit.sh
RUN chmod +x /usr/local/bin/start_bandit.sh
ENTRYPOINT ["/usr/local/bin/start_bandit.sh"]
