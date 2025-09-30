#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${BANDIT_LEVEL:-}" || -z "${BANDIT_PASSWORD:-}" ]]; then
  echo "❌ Falta definir BANDIT_LEVEL y/o BANDIT_PASSWORD."
  echo "Ejemplo: docker run -it -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD=bandit0 alastex/bandit-connector"
  exit 1
fi

echo "🔑 Conectando a Bandit nivel ${BANDIT_LEVEL} ..."
exec sshpass -p "$BANDIT_PASSWORD" ssh \
  -o StrictHostKeyChecking=no \
  -p 2220 "bandit${BANDIT_LEVEL}@bandit.labs.overthewire.org"

