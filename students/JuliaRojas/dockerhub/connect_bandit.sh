#!/bin/sh

if [ -z "$BANDIT_LEVEL" ] || [ -z "$BANDIT_PASS" ]; then
  echo "Error: Las variables BANDIT_LEVEL y BANDIT_PASS deben estar definidas."
  exit 1
fi

echo "Conectando a bandit$BANDIT_LEVEL.overthewire.org..."
echo "Usuario: bandit$BANDIT_LEVEL"

sshpass -p "$BANDIT_PASS" ssh -o StrictHostKeyChecking=no bandit$BANDIT_LEVEL@bandit.overthewire.org -p 2220
