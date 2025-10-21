#!/usr/bin/env bash
set -euo pipefail
: "${BANDIT_LEVEL:=}"
: "${BANDIT_PASS:=}"
BANDIT_HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
BANDIT_PORT="${BANDIT_PORT:-2220}"
if [[ -z "$BANDIT_LEVEL" || -z "$BANDIT_PASS" ]]; then
  echo "[ERROR] Debes definir BANDIT_LEVEL y BANDIT_PASS (con -e o --env-file)"
  echo "Ejemplo: docker run -it --rm -e BANDIT_LEVEL=0 -e BANDIT_PASS=bandit0 usuario/imagen"
  exit 1
fi
USER_ON_HOST="bandit${BANDIT_LEVEL}"
exec sshpass -p "$BANDIT_PASS" ssh -tt \
  -o StrictHostKeyChecking=accept-new \
  -p "$BANDIT_PORT" \
  "${USER_ON_HOST}@${BANDIT_HOST}"
