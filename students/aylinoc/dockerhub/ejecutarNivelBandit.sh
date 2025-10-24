#!/usr/bin/env bash
set -euo pipefail
BANDIT_USER="${BANDIT_USER:-}"
BANDIT_PASS="${BANDIT_PASS:-}"
BANDIT_HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
BANDIT_PORT="${BANDIT_PORT:-2220}"
if [ -z "$BANDIT_USER" ] || [ -z "$BANDIT_PASS" ]; then
  echo "Error: Las variables de entorno BANDIT_USER y BANDIT_PASS no están configuradas."
  echo "Ejemplo con -e: docker run -it -e BANDIT_USER=bandit0 -e BANDIT_PASS=xxxxx TU_IMAGEN"
  echo "Ejemplo con --env-file: docker run -it --env-file .env TU_IMAGEN"
  exit 1
fi
echo "Conectando a $BANDIT_USER@$BANDIT_HOST:$BANDIT_PORT ..."
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
exec sshpass -p "$BANDIT_PASS" ssh $SSH_OPTS -p "$BANDIT_PORT" -o PreferredAuthentications=password -o PubkeyAuthentication=no "$BANDIT_USER"@"$BANDIT_HOST"
EOF

chmod +x ejecutarNivelBandit.sh

