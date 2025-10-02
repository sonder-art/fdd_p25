#!/usr/bin/env bash
set -euo pipefail

# Acepta BANDIT_TARGET (preferido) y como alias BANDIT_LEVEL
BANDIT_TARGET="${BANDIT_TARGET:-${BANDIT_LEVEL:-}}"
: "${BANDIT_TARGET:?Falta BANDIT_TARGET}"

# Contraseña: preferimos la del nivel previo; como fallback, la directa
PASS="${BANDIT_PREV_PASSWORD:-${BANDIT_PASSWORD:-}}"
: "${PASS:?Falta BANDIT_PREV_PASSWORD (o BANDIT_PASSWORD)}"

HOST="bandit.labs.overthewire.org"
PORT=2220
USER="bandit${BANDIT_TARGET}"

echo "[INFO] Conectando a ${USER}@${HOST}:${PORT} ..."
REMOTE_CMD='whoami && pwd && exit'

sshpass -p "${PASS}" \
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    -p "${PORT}" "${USER}@${HOST}" "${REMOTE_CMD}"

echo "[OK] Conexión exitosa y comando remoto ejecutado."

