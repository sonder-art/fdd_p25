FROM alpine:3.20
RUN apk add --no-cache openssh-client sshpass bash
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENV LEVEL="" PASSWORD=""
ENTRYPOINT ["/app/entrypoint.sh"]

