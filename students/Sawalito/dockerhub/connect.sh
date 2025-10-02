#!/bin/sh

set -u

if [ -z "${BANDIT_LEVEL}" ] || [ -z "${BANDIT_PASSWORD}" ]; then
  echo " Error: Las variables de entorno BANDIT_LEVEL y BANDIT_PASSWORD son obligatorias." >&2
  echo "Ejemplo de uso:" >&2
  echo "docker run -it --rm -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD='...' tu-imagen" >&2
  exit 1
fi

echo "Intentando conectar a Bandit Nivel ${BANDIT_LEVEL}..."
echo "----------------------------------------------------"
echo "Host:   bandit.labs.overthewire.org"
echo "Usuario: bandit${BANDIT_LEVEL}"
echo "Puerto:  2220"
echo "----------------------------------------------------"

exec sshpass -p "${BANDIT_PASSWORD}" ssh -o StrictHostKeyChecking=no "bandit${BANDIT_LEVEL}@bandit.labs.overthewire.org" -p 2220
