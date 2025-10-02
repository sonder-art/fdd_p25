# Imagen base
FROM alpine:latest  

# Instalamos ssh + sshpass + bash
RUN apk add --no-cache openssh sshpass bash

# Copiamos el script con el nuevo nombre
COPY banditLogger.sh /usr/local/bin/banditLogger.sh
RUN chmod +x /usr/local/bin/banditLogger.sh

# Definimos el script como punto de entrada
ENTRYPOINT ["/usr/local/bin/banditLogger.sh"]


