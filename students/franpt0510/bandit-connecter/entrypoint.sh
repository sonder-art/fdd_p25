set -euo pipefail

: "${BANDIT_LEVEL:?Falta la variable de entorno BANDIT_LEVEL (ej. 0, 1, 2)}"
: "${BANDIT_PASSWORD:?Falta la variable de entorno BANDIT_PASSWORD}"
LEVEL="${BANDIT_LEVEL}"
PASS="${BANDIT_PASSWORD}"
HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
PORT="${BANDIT_PORT:-2220}"
USER="bandit${LEVEL}"
REMOTE_CMD=""
if [ "$#" -gt 0 ]; then
  REMOTE_CMD="$*"
fi
SSH_OPTS=(
  -p "$PORT"
  -o StrictHostKeyChecking=no
  -o UserKnownHostsFile=/dev/null
  -o LogLevel=ERROR
)
echo "Conectando a ${USER}@${HOST}:${PORT} ..."
if [ -n "$REMOTE_CMD" ]; then
  exec sshpass -p "$PASS" ssh "${SSH_OPTS[@]}" "${USER}@${HOST}" "$REMOTE_CMD"
else
  # Sesión interactiva
  exec sshpass -p "$PASS" ssh "${SSH_OPTS[@]}" "${USER}@${HOST}"
fi
