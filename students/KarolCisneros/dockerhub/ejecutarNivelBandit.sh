#!/bin/bash
set -euo pipefail

# LEE LAS VARIABLES DE ENTORNO (acepta que docker las pase con -e o --env-file)
BANDIT_USER="${BANDIT_USER:-}"
BANDIT_PASS="${BANDIT_PASS:-}"

# Verifica que existan
if [ -z "$BANDIT_USER" ] || [ -z "$BANDIT_PASS" ]; then
  echo "Error: Las variables de entorno BANDIT_USER y BANDIT_PASS no están configuradas."
  echo "Usa: docker run -e BANDIT_USER=bandit0 -e BANDIT_PASS=xxxxx imagen"
  exit 1
fi

echo "Iniciando conexión SSH para el usuario: $BANDIT_USER"


SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"


PORT=2220

exec sshpass -p "$BANDIT_PASS" ssh $SSH_OPTS -p "$PORT" -o PreferredAuthentications=password -o PubkeyAuthentication=no "$BANDIT_USER"@bandit.labs.overthewire.org

