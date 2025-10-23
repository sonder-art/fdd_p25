#!/bin/bash

set -euo pipefail
# set -e: si cualquier comando falla (sale ≠ 0), el script termina.
# set -u: usar una variable no definida provoca error (ayuda a detectar typos).
# set -o pipefail: si en un cmd1 | cmd2 falla cmd1, el pipeline falla (no se “traga” errores).

: "${BANDIT_NIVEL:?Falta la variable BANDIT_NIVEL (nivel numérico, ej. 0,1,2,...,34)}"
: "${BANDIT_PASS:?Falta la variable BANDIT_PASS (password del nivel)}"
# La expansión ${VAR:?mensaje} hace que, si VAR no está definida, el script aborte mostrando el mensaje.
# Aquí exigimos que existan BANDIT_NIVEL y BANDIT_PASS.

BANDIT_HOST="${BANDIT_HOST:-bandit.labs.overthewire.org}"
BANDIT_PORT="${BANDIT_PORT:-2220}"
#Si no defines BANDIT_HOST/BANDIT_PORT, usa esos por defecto.

if ! [[ "$BANDIT_NIVEL" =~ ^[0-9]+$ ]] || (( BANDIT_NIVEL < 0 || BANDIT_NIVEL > 34 )); then
  echo "El nivel deseado no existe (usa 0..34). Recibido: '$BANDIT_NIVEL'" >&2
  exit 1
fi


USER="bandit${BANDIT_NIVEL}"

echo "Conectando al nivel ${BANDIT_NIVEL}..."
echo "(usa Ctrl+C para salir)"

if (( $# > 0 )); then
# MODO NO INTERACTIVO: ejecuta el/los comando(s) pasados como argumentos y sale
  exec sshpass -p "$BANDIT_PASS" \
    ssh -p "$BANDIT_PORT" \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        "${USER}@${BANDIT_HOST}" -- "$@"
else
# MODO INTERACTIVO: abre una sesión con TTY
  exec sshpass -p "$BANDIT_PASS" \
    ssh -tt -p "$BANDIT_PORT" \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        "${USER}@${BANDIT_HOST}"
fi

