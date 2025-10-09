set -e

LEVEL="${BANDIT_LEVEL:-}"
PASS="${BANDIT_PASSWORD:-}"
HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
PORT="${BANDIT_PORT:-2220}"

if [ -z "$LEVEL" ] || [ -z "$PASS" ]; then
  echo "Error: Debes definir BANDIT_LEVEL y BANDIT_PASSWORD."
  echo "Ejemplo: -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD='bandit0'"
  exit 1
fi

case "$LEVEL" in
  ''|*[!0-9]*)
    echo "Error: BANDIT_LEVEL debe ser un entero (0,1,2,...) — Recibido: '$LEVEL'"
    exit 1
    ;;
esac

USER="bandit$LEVEL"

echo "Conectando a $HOST:$PORT como $USER ..."
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $PORT -tt"

if [ "$#" -gt 0 ]; then
  exec sshpass -p "$PASS" ssh $SSH_OPTS "$USER@$HOST" -- "$@"
else
  exec sshpass -p "$PASS" ssh $SSH_OPTS "$USER@$HOST"
fi
