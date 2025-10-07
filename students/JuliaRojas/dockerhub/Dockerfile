FROM alpine:latest

RUN apk add --no-cache sshpass openssh-client

WORKDIR /app

COPY connect_bandit.sh .

RUN chmod +x connect_bandit.sh 

ENTRYPOINT ["./connect_bandit.sh"]
