#!/bin/bash
set -e

# Leer variables de entorno
NIVEL=${BANDIT_LEVEL}
PASSWORD=${BANDIT_PASSWORD}

# Validar
if [[ -z "$NIVEL" || -z "$PASSWORD" ]]; then
  echo "❌ Error: Debes definir BANDIT_LEVEL y BANDIT_PASSWORD"
  exit 1
fi

echo "🔑 Conectando a Bandit nivel $NIVEL ..."

# Usuario de bandit
USER="bandit${NIVEL}"

# Usar sshpass para entrar automáticamente
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no ${USER}@bandit.labs.overthewire.org -p 2220

