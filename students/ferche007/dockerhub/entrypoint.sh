#!/usr/bin/env bash
set -euo pipefail
: "${LEVEL:?Falta LEVEL (ej. 0,1,2,...)}"
: "${PASSWORD:?Falta PASSWORD}"
HOST="bandit.labs.overthewire.org" 
PORT="2220"  
USER="bandit${LEVEL}"
echo "Conectando a ${USER}@${HOST}:${PORT} ..."
echo "Recuerda ejecutar el contenedor con -it para tener terminal interactiva."
sshpass -p "${PASSWORD}" \
  ssh -o StrictHostKeyChecking=accept-new -p "${PORT}" "${USER}@${HOST}"
