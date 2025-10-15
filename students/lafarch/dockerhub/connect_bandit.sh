#!/bin/bash

# Verificar que las variables de entorno estén definidas
if [ -z "$BANDIT_LEVEL" ] || [ -z "$BANDIT_PASSWORD" ]; then
    echo "Error: Debes proporcionar BANDIT_LEVEL y BANDIT_PASSWORD"
    echo "Ejemplo: docker run -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD=bandit0 ..."
    exit 1
fi

# Construir el nombre de usuario
USERNAME="bandit${BANDIT_LEVEL}"
HOST="bandit.labs.overthewire.org"
PORT=2220

echo "Conectando a Bandit nivel ${BANDIT_LEVEL}..."
echo "Usuario: ${USERNAME}"
echo "Host: ${HOST}"
echo ""

# Usar sshpass para conectarse automáticamente
# Cuando la conexión SSH termina, el script también termina
sshpass -p "${BANDIT_PASSWORD}" ssh -o StrictHostKeyChecking=no -p ${PORT} ${USERNAME}@${HOST}

# Capturar el código de salida de SSH
SSH_EXIT_CODE=$?

# Salir con el mismo código
exit $SSH_EXIT_CODE
