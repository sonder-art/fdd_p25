#!/usr/bin/env bash
set -euo pipefail
info()  { printf "\033[1;34m[INFO]\033[0m %s\n" "$*"; }
warn()  { printf "\033[1;33m[WARN]\033[0m %s\n" "$*"; }
error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$*" >&2; }

if [[ -z "${BANDIT_LEVEL:-}" ]]; then
  error "Falta BANDIT_LEVEL (ej. 0, 1, 2, ...). Pásala con -e o --env-file."
  exit 1
fi
if [[ -z "${BANDIT_PASSWORD:-}" ]]; then
  error "Falta BANDIT_PASSWORD para bandit${BANDIT_LEVEL}."
  exit 1
fi

BANDIT_HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
BANDIT_PORT="${BANDIT_PORT:-2220}"
BANDIT_COMMAND="${BANDIT_COMMAND:-}"
USER_NAME="bandit${BANDIT_LEVEL}"

info "Conectando a ${USER_NAME}@${BANDIT_HOST}:${BANDIT_PORT} ..."
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

if [[ -n "${BANDIT_COMMAND}" ]]; then
  info "Ejecutando comando remoto: ${BANDIT_COMMAND}"
  exec sshpass -p "${BANDIT_PASSWORD}" \
    ssh ${SSH_OPTS} -p "${BANDIT_PORT}" "${USER_NAME}@${BANDIT_HOST}" \
    "${BANDIT_COMMAND}"
else
  warn "No se proporcionó BANDIT_COMMAND; abriendo sesión interactiva."
  exec sshpass -p "${BANDIT_PASSWORD}" \
    ssh ${SSH_OPTS} -p "${BANDIT_PORT}" "${USER_NAME}@${BANDIT_HOST}"
fi
