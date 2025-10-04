
FROM alpine:latest

RUN apk add --no-cache bash openssh sshpass

COPY ejecutarNivelBandit.sh /usr/local/bin/ejecutarNivelBandit.sh 

RUN chmod +x /usr/local/bin/ejecutarNivelBandit.sh

ENTRYPOINT ["/usr/local/bin/ejecutarNivelBandit.sh"]

