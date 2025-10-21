#!/usr/bin/env bash
set -euo pipefail

# Requeridos
: "${BANDIT_LEVEL:?Falta la variable BANDIT_LEVEL}"
: "${BANDIT_PASS:?Falta la variable BANDIT_PASS}"

# Opcionales
BANDIT_HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
BANDIT_PORT="${BANDIT_PORT:-2220}"

USER="bandit${BANDIT_LEVEL}"
echo "🔐 Conectando a ${USER}@${BANDIT_HOST}:${BANDIT_PORT} (nivel ${BANDIT_LEVEL})"

# SSH sin preguntar fingerprint; -t para TTY interactivo
exec sshpass -p "${BANDIT_PASS}" \
  ssh -o StrictHostKeyChecking=no -p "${BANDIT_PORT}" -t "${USER}@${BANDIT_HOST}"
