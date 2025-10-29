# 1. Imagen base
FROM alpine:latest

# 2. Intalo herramientas
# instalamos bash, cliente openssh y sshpass
RUN apk add --no-cache bash openssh sshpass

# 3. Copio el script
COPY ejecutarNivelBandit.sh /usr/local/bin/ejecutarNivelBandit.sh

# 4. Permiso de ejecución
RUN chmod +x /usr/local/bin/ejecutarNivelBandit.sh

# 5. Ejecuto el script 
ENTRYPOINT ["/usr/local/bin/ejecutarNivelBandit.sh"]

