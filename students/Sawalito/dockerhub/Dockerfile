FROM alpine:3.20

LABEL maintainer="tu_nombre_de_usuario"
LABEL description="Un contenedor para conectarse fácilmente a los niveles del wargame Bandit."

RUN apk add --no-cache openssh-client sshpass

WORKDIR /app

COPY connect.sh .
RUN chmod +x connect.sh

ENTRYPOINT ["./connect.sh"]
