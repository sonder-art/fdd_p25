#!/usr/bin/env bash 
set -euo pipefail

: "${BANDIT_LEVEL:?Debes exportar BANDIT_LEVEL}"
: "${BANDIT_PASSWORD:?Debes exportar BANDIT_PASSWORD}"

USER="bandit${BANDIT_LEVEL}"
HOST="bandit.labs.overthewire.org"
PORT="${BANDIT_PORT:-2220}"

echo "==> Conectando a ${USER}@${HOST}:${PORT} ..."
sshpass -p "${BANDIT_PASSWORD}" ssh \
  -p "${PORT}" \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  "${USER}@${HOST}" \
  'echo "Autenticado como: $(whoami)"; uname -a; ls -la'

echo "==> Sesión finalizada correctamente."
