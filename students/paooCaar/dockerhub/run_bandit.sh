#!/bin/sh

if [ -z "$BANDIT_LEVEL" ] || [ -z "$BANDIT_PASS" ]; then
  echo "❌ Error: debes definir BANDIT_LEVEL y BANDIT_PASS"
  exit 1
fi

echo "➡️ Conectando a Bandit nivel $BANDIT_LEVEL ..."
sshpass -p "$BANDIT_PASS" ssh -o StrictHostKeyChecking=no bandit$BANDIT_LEVEL@bandit.labs.overthewire.org -p 2220
