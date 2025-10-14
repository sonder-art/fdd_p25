#!/usr/bin/env bash

LEVEL="${BANDIT_LEVEL:-}"
PASS="${BANDIT_PASSWORD:-}"
HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
PORT="${BANDIT_PORT:-2220}"

if [[ -z "$LEVEL" || -z "$PASS" ]]; then
  echo " Faltan variables: debes exportar BANDIT_LEVEL y BANDIT_PASSWORD."
  echo "   Ejemplo: -e BANDIT_LEVEL=5 -e BANDIT_PASSWORD=pepe"
  echo "   O bien:  --env-file .env"
  exit 1
fi

USER="bandit${LEVEL}"
echo "Conectando a ${USER}@${HOST}:${PORT} ..."
exec sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -p "$PORT" "${USER}@${HOST}"
