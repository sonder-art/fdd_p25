#!/bin/bash
# script.sh


if [ -z "$BANDIT_LEVEL" ] || [ -z "$BANDIT_PASS" ]; then
	  echo "ERROR: Debes pasar BANDIT_LEVEL y BANDIT_PASS como variables de entorno."
	    exit 1
fi

echo "Conectando a Bandit Level $BANDIT_LEVEL..."

sshpass -p "$BANDIT_PASS" ssh -o StrictHostKeyChecking=no bandit$BANDIT_LEVEL@bandit.labs.overthewire.org -p 2220

