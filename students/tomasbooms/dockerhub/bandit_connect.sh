#!/bin/bash

# Script para conectarse a los niveles de Bandit
# Lee las variables de entorno BANDIT_LEVEL y BANDIT_PASSWORD

# Verificar que las variables de entorno estén configuradas
if [ -z "$BANDIT_LEVEL" ]; then
    echo "Error: La variable BANDIT_LEVEL no está configurada."
    echo "Uso: docker run -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD=bandit0 <imagen>"
    exit 1
fi

if [ -z "$BANDIT_PASSWORD" ]; then
    echo "Error: La variable BANDIT_PASSWORD no está configurada."
    echo "Uso: docker run -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD=bandit0 <imagen>"
    exit 1
fi

# Configurar el host y usuario de Bandit
BANDIT_HOST="bandit.labs.overthewire.org"
BANDIT_PORT="2220"
BANDIT_USER="bandit${BANDIT_LEVEL}"

echo "======================================"
echo "Conectando a Bandit Nivel ${BANDIT_LEVEL}"
echo "Usuario: ${BANDIT_USER}"
echo "Host: ${BANDIT_HOST}:${BANDIT_PORT}"
echo "======================================"
echo ""

# Conectar usando sshpass para pasar la contraseña automáticamente
# -o StrictHostKeyChecking=no: Evita la verificación de la clave del host
# -o UserKnownHostsFile=/dev/null: No guarda el host en known_hosts
sshpass -p "${BANDIT_PASSWORD}" ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -p ${BANDIT_PORT} \
    ${BANDIT_USER}@${BANDIT_HOST}

# Capturar el código de salida
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "======================================"
    echo "Error al conectar. Verifica:"
    echo "- El nivel especificado es correcto"
    echo "- La contraseña es correcta"
    echo "- Tienes conexión a internet"
    echo "======================================"
fi

exit $EXIT_CODE
