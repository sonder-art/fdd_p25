FROM alpine:latest


# Actualizamos los repositorios de paquetes e instalamos las dependencias.
RUN apk update && apk add --no-cache openssh-client sshpass

# Establecemos el directorio de trabajo como /app
WORKDIR /app

# Copiamos nuestro script de shell desde el contexto de build (tu máquina)
# al directorio de trabajo del contenedor.
COPY bandit.sh .

# Nos aseguramos de que el script tenga permisos de ejecución dentro de la imagen.
RUN chmod +x ./bandit.sh

# El ENTRYPOINT define el comando que se ejecutará cuando el contenedor inicie.
# Al usar el formato "exec" (con corchetes), se ejecuta directamente,
# sin un shell intermedio, lo cual es más eficiente.
ENTRYPOINT ["./bandit.sh"]
