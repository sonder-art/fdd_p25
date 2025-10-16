#!/bin/bash

# Leer variables de entorno
BANDIT_LEVEL=${BANDIT_LEVEL}
BANDIT_PASS=${BANDIT_PASS}

# Validar que estén definidas
if [ -z "$BANDIT_LEVEL" ] || [ -z "$BANDIT_PASS" ]; then
  echo "Por favor define BANDIT_LEVEL y BANDIT_PASS"
  exit 1
fi

# Conectarse al nivel correspondiente de Bandit usando ssh
echo "Conectando a Bandit nivel $BANDIT_LEVEL..."
ssh bandit$BANDIT_LEVEL@bandit.labs.overthewire.org -p 2220 -i /path/to/private_key "echo $BANDIT_PASS"

