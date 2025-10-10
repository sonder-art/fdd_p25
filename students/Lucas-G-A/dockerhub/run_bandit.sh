#!/usr/bin/env bash
set -euo pipefail

: "${BANDIT_LEVEL:?Debes definir BANDIT_LEVEL (ej. 0, 1, 2...)}"
: "${BANDIT_PASSWORD:?Debes definir BANDIT_PASSWORD (la contraseña del nivel)}"

BANDIT_HOST="bandit.labs.overthewire.org"
BANDIT_PORT=2220
BANDIT_USER="bandit${BANDIT_LEVEL}"

echo "[INFO] Conectando a ${BANDIT_USER}@${BANDIT_HOST}:${BANDIT_PORT} ..."

mkdir -p ~/.ssh
touch ~/.ssh/known_hosts
ssh-keyscan -p "${BANDIT_PORT}" "${BANDIT_HOST}" >> ~/.ssh/known_hosts 2>/dev/null || true

exec sshpass -p "${BANDIT_PASSWORD}" ssh \
  -p "${BANDIT_PORT}" \
  -o StrictHostKeyChecking=accept-new \
  "${BANDIT_USER}@${BANDIT_HOST}"
